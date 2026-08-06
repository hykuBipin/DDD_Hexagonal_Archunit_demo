def get_recovery_advice(excess_calories: int, no_sugar: bool = False, no_garlic: bool = False, gluten_free: bool = False) -> dict:
    """
    Returns positive, encouraging caretaker suggestions.
    Food is joy! Never restrict or block orders, keep suggestions positive.
    """
    recommendations = []

    # Apply preference-specific caretaker tips
    if no_sugar:
        recommendations.append("🍬 Unsweetened Choice: Swap added sugar items for fresh stevia mint juice or black coffee.")
    if no_garlic:
        recommendations.append("🧅 Sattvik Diet: Choose dishes made without garlic/onion, or instruct kitchen to omit them.")
    if gluten_free:
        recommendations.append("🌾 Gluten-free alternative: Opt for brown rice or millet flatbreads instead of standard wheat flour.")

    # General digestion/metabolic support recommendations
    recommendations.append("💧 Hydration: Drink warm lemon water or mint tea to aid comfortable digestion.")
    recommendations.append("😴 Metabolic Rest: Ensure a quality 7-8 hours of sleep tonight to regulate hormones naturally.")

    # Exercise suggestions based on excess calories
    if excess_calories > 0:
        if excess_calories < 150:
            recommendations.append("🚶 Stroll: Try a gentle 10-minute walk after your meal to help with initial digestion.")
        elif excess_calories <= 300:
            recommendations.append("🚶 Walk: A pleasant 15-20 minute post-meal evening walk is a great way to stay light.")
            recommendations.append("🏃 Movement: 3 sets of 10 light jumping jacks to keep active, if you feel comfortable.")
        else:
            recommendations.append("🚶 Walk: A gentle 25-30 minute active walk helps keep energy balanced.")
            recommendations.append("🏃 Movement: 3 sets of 12 light jumping jacks to stay refreshed.")
    else:
        recommendations.append("⭐ Goal Match: You are perfectly aligned with your selected calorie threshold!")

    return {
        "title": "Dieto Positive Caretaker Tips 🌟",
        "message": f"Food is joy and energy! You are fully supported to order whatever you like. Here are gentle, healthy tips based on your profile:",
        "recommendations": recommendations
    }
