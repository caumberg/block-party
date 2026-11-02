-- Block Party token economy v1
-- Run once in Supabase SQL Editor after reviewing.
-- Existing leaderboard tables are not changed by this migration.

create table if not exists public.players (
  id uuid primary key references auth.users(id) on delete cascade,
  solo_name varchar(20),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint players_solo_name_valid check (
    solo_name is null or length(btrim(solo_name)) between 1 and 20
  )
);

create table if not exists public.player_wallets (
  player_id uuid primary key references public.players(id) on delete cascade,
  balance integer not null default 0 check (balance >= 0),
  updated_at timestamptz not null default now()
);

create table if not exists public.token_transactions (
  id uuid primary key default gen_random_uuid(),
  player_id uuid not null references public.players(id) on delete cascade,
  delta integer not null check (delta <> 0),
  balance_after integer not null check (balance_after >= 0),
  reason text not null check (reason in ('welcome','game_entry','refund','reward','purchase','adjustment')),
  reference_id uuid,
  created_at timestamptz not null default now()
);
create unique index if not exists token_transactions_reason_reference_unique
  on public.token_transactions(player_id, reason, reference_id)
  where reference_id is not null;
create index if not exists token_transactions_player_date
  on public.token_transactions(player_id, created_at desc);

create table if not exists public.game_sessions (
  id uuid primary key,
  player_id uuid not null references public.players(id) on delete cascade,
  game_mode text not null check (game_mode in (
    'line','timed-90','timed-180','timed-300','unlimited',
    'versus-easy','versus-medium','versus-hard'
  )),
  tokens_charged integer not null default 2 check (tokens_charged = 2),
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  constraint game_sessions_player_id_unique unique (player_id,id)
);
create index if not exists game_sessions_player_started
  on public.game_sessions(player_id, started_at desc);

-- Give each newly authenticated user one wallet and one welcome grant.
-- Supabase anonymous auth users are real auth.users records.
create or replace function public.create_block_party_player()
returns trigger
language plpgsql security definer
set search_path = ''
as $$
begin
  insert into public.players(id) values (new.id)
    on conflict (id) do nothing;
  insert into public.player_wallets(player_id, balance)
    values (new.id, 20)
    on conflict (player_id) do nothing;
  insert into public.token_transactions(player_id, delta, balance_after, reason)
    select new.id, 20, 20, 'welcome'
    where not exists (
      select 1 from public.token_transactions
      where player_id = new.id and reason = 'welcome'
    );
  return new;
end;
$$;

drop trigger if exists block_party_new_auth_user on auth.users;
create trigger block_party_new_auth_user
after insert on auth.users
for each row execute function public.create_block_party_player();

-- Atomic, idempotent game entry: charge once for each unique session UUID.
create or replace function public.start_block_party_game(
  p_session_id uuid,
  p_game_mode text
)
returns table(session_id uuid, remaining_tokens integer)
language plpgsql security definer
set search_path = ''
as $$
declare
  v_user uuid := auth.uid();
  v_balance integer;
  v_existing public.game_sessions%rowtype;
begin
  if v_user is null then
    raise exception 'Authentication required';
  end if;
  if p_session_id is null or p_game_mode not in (
    'line','timed-90','timed-180','timed-300','unlimited',
    'versus-easy','versus-medium','versus-hard'
  ) or p_game_mode is null then
    raise exception 'Invalid session or game mode';
  end if;

  -- Serializes requests for this player's wallet.
  select balance into v_balance
  from public.player_wallets
  where player_id = v_user
  for update;
  if not found then raise exception 'Wallet not found'; end if;

  select * into v_existing
  from public.game_sessions
  where id = p_session_id;
  if found then
    if v_existing.player_id <> v_user or v_existing.game_mode <> p_game_mode then
      raise exception 'Session ID already used';
    end if;
    session_id := p_session_id;
    remaining_tokens := v_balance;
    return next;
    return;
  end if;

  if v_balance < 2 then
    raise exception 'Insufficient tokens';
  end if;

  insert into public.game_sessions(id,player_id,game_mode)
  values (p_session_id,v_user,p_game_mode);
  update public.player_wallets
  set balance = balance - 2, updated_at = now()
  where player_id = v_user
  returning balance into v_balance;
  insert into public.token_transactions(player_id,delta,balance_after,reason,reference_id)
  values (v_user,-2,v_balance,'game_entry',p_session_id);

  session_id := p_session_id;
  remaining_tokens := v_balance;
  return next;
end;
$$;

-- Optional authenticated name update, independent of the leaderboard display snapshot.
create or replace function public.set_block_party_solo_name(p_name text)
returns void
language plpgsql security definer
set search_path = ''
as $$
begin
  if auth.uid() is null then raise exception 'Authentication required'; end if;
  if p_name is null or length(btrim(p_name)) not between 1 and 20 then
    raise exception 'Solo name must be 1-20 characters';
  end if;
  update public.players
  set solo_name = btrim(p_name), updated_at = now()
  where id = auth.uid();
end;
$$;

alter table public.players enable row level security;
alter table public.player_wallets enable row level security;
alter table public.token_transactions enable row level security;
alter table public.game_sessions enable row level security;

drop policy if exists players_read_own on public.players;
create policy players_read_own on public.players for select to authenticated
using (id = (select auth.uid()));
drop policy if exists wallets_read_own on public.player_wallets;
create policy wallets_read_own on public.player_wallets for select to authenticated
using (player_id = (select auth.uid()));
drop policy if exists transactions_read_own on public.token_transactions;
create policy transactions_read_own on public.token_transactions for select to authenticated
using (player_id = (select auth.uid()));
drop policy if exists sessions_read_own on public.game_sessions;
create policy sessions_read_own on public.game_sessions for select to authenticated
using (player_id = (select auth.uid()));

revoke all on public.players, public.player_wallets, public.token_transactions, public.game_sessions from anon, authenticated;
grant select on public.players, public.player_wallets, public.token_transactions, public.game_sessions to authenticated;
revoke all on function public.start_block_party_game(uuid,text) from public, anon;
revoke all on function public.set_block_party_solo_name(text) from public, anon;
grant execute on function public.start_block_party_game(uuid,text) to authenticated;
grant execute on function public.set_block_party_solo_name(text) to authenticated;

-- Later: add leaderboard_scores.player_id with a FK after client integration is verified.
-- Do not infer player IDs from existing player_name values.
