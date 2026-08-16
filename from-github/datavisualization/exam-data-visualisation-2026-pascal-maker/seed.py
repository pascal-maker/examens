from backend.database import SessionLocal, init_database
from backend.services import seed_demo_data


def main():
    init_database()
    with SessionLocal() as session:
        seed_demo_data(session)
        session.commit()
    print("Demo data seeded successfully.")


if __name__ == "__main__":
    main()
