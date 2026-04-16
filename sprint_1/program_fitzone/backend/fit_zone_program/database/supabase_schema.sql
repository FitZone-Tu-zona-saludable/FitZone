create table if not exists users (
    user_id bigserial primary key,
    user_name text not null,
    user_email text not null unique,
    user_password text not null,
    user_role text not null,
    user_status text not null default 'active'
);

create table if not exists memberships (
    membership_id bigserial primary key,
    user_id bigint not null references users(user_id) on delete cascade,
    membership_plan text not null,
    membership_price numeric(12, 2) not null,
    membership_duration integer not null,
    membership_benefits text,
    membership_status text not null default 'active'
);

create table if not exists payments (
    payment_id bigserial primary key,
    user_id bigint not null references users(user_id) on delete cascade,
    membership_id bigint not null references memberships(membership_id) on delete cascade,
    payment_amount numeric(12, 2) not null,
    payment_date date not null,
    payment_method text not null,
    payment_reference text not null,
    payment_status text not null default 'pending'
);

create table if not exists access_logs (
    log_id bigserial primary key,
    user_email text not null,
    action text not null,
    result text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_users_email on users(user_email);
create index if not exists idx_memberships_user_id on memberships(user_id);
create index if not exists idx_payments_user_id on payments(user_id);
create index if not exists idx_payments_membership_id on payments(membership_id);
