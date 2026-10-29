import argparse
import asyncio

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.models import ApiKey, Tenant
from app.core.security import generate_api_key


async def create_tenant(name: str) -> None:
    async with SessionLocal() as session:
        tenant = Tenant(name=name)
        session.add(tenant)
        await session.commit()
        print(f"tenant criado: {tenant.id}")


async def create_key(tenant_name: str, key_name: str) -> None:
    async with SessionLocal() as session:
        tenant = await session.scalar(select(Tenant).where(Tenant.name == tenant_name))
        if tenant is None:
            raise SystemExit(f"tenant '{tenant_name}' não existe")

        full_key, prefix, key_hash = generate_api_key()
        session.add(ApiKey(tenant_id=tenant.id, name=key_name, prefix=prefix, key_hash=key_hash))
        await session.commit()

        print("GUARDE AGORA, não será mostrada de novo:")
        print(full_key)


def main() -> None:
    parser = argparse.ArgumentParser(prog="platform-cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("create-tenant")
    t.add_argument("name")

    k = sub.add_parser("create-key")
    k.add_argument("tenant")
    k.add_argument("--name", default="default")

    args = parser.parse_args()
    if args.cmd == "create-tenant":
        asyncio.run(create_tenant(args.name))
    else:
        asyncio.run(create_key(args.tenant, args.name))


if __name__ == "__main__":
    main()
