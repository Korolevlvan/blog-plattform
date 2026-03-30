import argparse
from sqlalchemy import create_engine, text

def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate users from old monolith DB to users-api DB")
    parser.add_argument("--source", required=True, help="Source database URL")
    parser.add_argument("--target", required=True, help="Target users database URL")
    args = parser.parse_args()

    source_engine = create_engine(args.source)
    target_engine = create_engine(args.target)

    with source_engine.begin() as source_conn, target_engine.begin() as target_conn:
        rows = source_conn.execute(text(
            "SELECT id, email, username, password_hash, bio, image_url, created_at, updated_at FROM users ORDER BY id"
        )).mappings().all()

        for row in rows:
            target_conn.execute(text(
                '''
                INSERT INTO users (id, email, username, password_hash, bio, image_url, created_at, updated_at)
                VALUES (:id, :email, :username, :password_hash, :bio, :image_url, :created_at, :updated_at)
                ON CONFLICT (id) DO NOTHING
                '''
            ), dict(row))

    print(f"Migrated {len(rows)} users")

if __name__ == "__main__":
    main()
