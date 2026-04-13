def format_status(status: str, retries: int) -> str:
    return f"status={status} retries={retries}"


status = "pending"
print(format_status("pending", 1))
