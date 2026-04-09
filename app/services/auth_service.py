class AuthService:

    @staticmethod
    async def process_login(data: dict):
        username = data.get("username")
        password = data.get("password")

        # Step 1: Username check
        if username != "admin":
            return {"status": "failure", "message": "Invalid username"}

        # Step 2: Ask for password
        if not password:
            return {"status": "need_password"}

        # Step 3: Validate password
        if password == "admin123":
            return {"status": "success"}

        return {"status": "failure", "message": "Wrong password"}