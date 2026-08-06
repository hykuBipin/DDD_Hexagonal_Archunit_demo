def get_recovery_advice(
    excess_calories: int, 
    no_sugar: bool = False, 
    no_garlic: bool = False, 
    gluten_free: bool = False,
    cart_items: list = None
) -> dict:
    """
    Generates highly dynamic and positive wellness recommendations.
    Never restricts or blocks ordering, keeping suggestions constructive.
    """
    if cart_items is None:
        cart_items = []

    recommendations = []
    
    # 1. Dynamic item-specific suggestions mapped to preferences
    for item in cart_items:
        item_lower = item.lower()
        if "burger" in item_lower:
            recommendations.append("🍔 Comfort Choice: Enjoy your burger! To balance its heavy fats, you might enjoy pairing it with mineral water instead of a sugary beverage.")
            if gluten_free:
                recommendations.append("🌾 Gluten Alternative: Request the restaurant to serve the burger bun-less (lettuce-wrapped) to keep it 100% gluten-free.")
        
        elif "soda" in item_lower:
            if no_sugar:
                recommendations.append("🍬 Added Sugar Swap: Lime Soda contains sucrose. Swap for fresh Mint Juice sweetened with stevia to save 75 calories.")
            else:
                recommendations.append("🥤 Hydration Tip: Enjoy your soda! Consider sipping a glass of water alongside it to keep hydration levels balanced.")
                
        elif "wrap" in item_lower or "roll" in item_lower:
            if gluten_free:
                recommendations.append("🌾 Gluten Notice: Wraps typically use wheat flour flatbreads. Ask for a gluten-free millet roti option.")
            else:
                recommendations.append("🌯 Wrap Choice: Rich in protein! A great fuel source for your muscles today.")
                
        elif "bowl" in item_lower or "biryani" in item_lower:
            if no_garlic:
                recommendations.append("🧅 Sattvik Diet: Add a note on Swiggy to request the restaurant to omit garlic/onion paste in the rice bowl gravy.")
            else:
                recommendations.append("🍲 Bowl Choice: A hearty meal! Take your time eating to support natural satiety cues.")
                
        elif "salad" in item_lower:
            recommendations.append("🥗 Fresh Pick: Excellent tandoori salad choice! Packed with high-quality lean protein and fiber.")

    # 2. General caretaker support tips
    recommendations.append("💧 Hydration: Drink a glass of warm lemon-mint water to aid digestion.")
    recommendations.append("😴 Metabolic Rest: Ensure a quality 7-8 hours of sleep tonight to regulate hormones naturally.")

    # 3. Dynamic exercise offsets based on calorie limits
    if excess_calories > 0:
        if excess_calories < 150:
            recommendations.append(f"🚶 Stroll: Try a gentle 10-minute walk after your meal to help with comfortable digestion (+{excess_calories} kcal offset).")
        elif excess_calories <= 300:
            recommendations.append("🚶 Walk: A pleasant 15-20 minute post-meal evening walk is a great way to stay light.")
            recommendations.append("🏃 Movement: 3 sets of 10 light jumping jacks to stay active, if you feel comfortable.")
        else:
            recommendations.append("🚶 Walk: A gentle 25-30 minute active walk helps keep energy balanced.")
            recommendations.append("🏃 Movement: 3 sets of 12 light jumping jacks to stay refreshed.")
    else:
        recommendations.append("⭐ Goal Match: You are perfectly aligned with your selected calorie threshold!")

    return {
        "title": "Dieto Caretaker Wellness Tips 🌟",
        "message": "Food is joy and fuel! We encourage you to enjoy your meal. Here are encouraging wellness tips based on your menu selection and profile preferences:",
        "recommendations": recommendations
    }
