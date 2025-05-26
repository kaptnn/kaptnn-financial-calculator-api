import base64
import bcrypt
from datetime import datetime, timedelta
from app.core.config import configs
from app.core.database import Database
from app.schema.user_schema import UpdateUserProfileRequest, User
from app.schema.company_schema import Company
from app.repositories.user_repo import UserRepository
from app.repositories.company_repo import CompanyRepository
from app.models.profile_model import Role, Membership

db = Database(configs.DB_URI)
company_repo = CompanyRepository(db.session)
user_repo = UserRepository(db.session)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return base64.b64encode(hashed).decode("utf-8")

def seed_super_company(company_name: str) -> Company:
    existing = company_repo.get_company_by_options("company_name", company_name)
    if existing.result:
        print(f"Company '{company_name}' already exists.")
        return existing.result

    year_now = datetime.now().year
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365 * 10)

    company = company_repo.create_company(
        company_name=company_name,
        year_of_assignment=year_now,
        start_audit_period=start_date,
        end_audit_period=end_date
    )
    print(f"✅ Company '{company_name}' seeded.")
    return company

def seed_super_admin(name: str, email: str, password: str, company_id: int) -> None:
    existing = user_repo.get_user_by_options("email", email)
    if existing.result:
        print(f"Superadmin with email '{email}' already exists.")
        return

    user: User = user_repo.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        company_id=company_id
    )

    profile_info = UpdateUserProfileRequest(
        role=Role.admin,
        membership_status=Membership.enterprise,
        is_verified=True
    )

    user_repo.create_user_profile(user.id)

    user_repo.update_user_profile(user.id, profile_info)
    print(f"✅ Superadmin '{email}' seeded.")

if __name__ == "__main__":
    try:
        company = seed_super_company(configs.SUPER_ADMIN_COMPANY_NAME)
        seed_super_admin(
            name=configs.SUPER_ADMIN_NAME,
            email=configs.SUPER_ADMIN_EMAIL,
            password=configs.SUPER_ADMIN_PASSWORD,
            company_id=company.id
        )
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
