def normalize_phone_number(phone: str) -> str:
    """
    Standardizes a phone number to E.164 format.
    Specifically handles New Zealand numbers by removing the leading 0.
    
    Example: 
    +640210000000 -> +64210000000
    0210000000 -> +64210000000
    """
    if not phone:
        return phone
        
    # Strip spaces
    phone = phone.replace(" ", "")
    
    # If the user inputted without country code but with leading zero
    if phone.startswith("02"):
        return "+64" + phone[1:]
        
    # If the frontend prepended +64 to a number with a leading zero
    if phone.startswith("+640"):
        return "+64" + phone[4:]
        
    return phone
