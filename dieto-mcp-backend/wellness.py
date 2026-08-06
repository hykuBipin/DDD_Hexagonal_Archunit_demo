def get_recovery_advice(excess_calories: int) -> dict:
    """
    Returns non-judgmental wellness and recovery suggestions when daily calorie limits are exceeded.
    Supports gentle movement, walks, sleep, and hydration rather than aggressive compensation.
    """
    if excess_calories <= 0:
        return {
            "title": "Healthy Boundaries Maintained! 🎉",
            "message": "You are within your target diet limits. Enjoy your meal!",
            "recommendations": [
                "💧 Continue normal hydration",
                "😴 Maintain standard rest patterns"
            ]
        }

    suggestions = [
        "💧 Hydrate with plain water or warm lemon-mint infusion to assist metabolism.",
        "😴 Focus on getting a sound 7-8 hours of sleep tonight to regulate hunger hormones.",
        "🥗 Plan a lighter next meal (such as vegetable clear soup or raw greens) to offset naturally."
    ]

    if excess_calories < 150:
        message = f"You are slightly above your calorie budget (+{excess_calories} kcal). Keep a normal routine!"
        suggestions.insert(0, "🚶 Take a 10-minute stroll to aid digestion.")
    elif excess_calories <= 300:
        message = f"You're currently {excess_calories} kcal over today's target. Let's make gentle choices for the next meal."
        suggestions.insert(0, "🚶 Try an easy 15-20 minute post-meal walk in the evening.")
        suggestions.append("🧘 Optional light activity: 3 × 10 jumping jacks or gentle stretching, if comfortable.")
    else:
        message = f"You're {excess_calories} kcal above today's goal. Focus on simple caretakers habits."
        suggestions.insert(0, "🚶 Take a 25-30 minute light walk to stay active.")
        suggestions.append("🧘 Optional light activity: 3 × 12 jumping jacks or minor stretching routines, if comfortable.")

    return {
        "title": "Flexible Meal Caretaker Plan 🎉",
        "message": message,
        "recommendations": suggestions
    }
