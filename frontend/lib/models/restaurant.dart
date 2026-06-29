class MatchedRestaurant {
  final String id;
  final String name;
  final double? avgRating;
  final String? totalRatings;
  final int? deliveryTimeMinutes;
  final String? deliveryTimeRange;
  final String? costForTwo;
  final String? availabilityStatus;
  final String? nextOpenTime;
  final String? imageUrl;
  final List<String> cuisines;
  final String? areaName;
  final double? distanceKm;
  final List<String> matchedPreferences;
  final String appDeepLink;
  final String webUrl;
  final String? offer;

  const MatchedRestaurant({
    required this.id,
    required this.name,
    this.avgRating,
    this.totalRatings,
    this.deliveryTimeMinutes,
    this.deliveryTimeRange,
    this.costForTwo,
    this.availabilityStatus,
    this.nextOpenTime,
    this.imageUrl,
    required this.cuisines,
    this.areaName,
    this.distanceKm,
    required this.matchedPreferences,
    required this.appDeepLink,
    required this.webUrl,
    this.offer,
  });

  factory MatchedRestaurant.fromJson(Map<String, dynamic> json) =>
      MatchedRestaurant(
        id: json['id'] as String,
        name: json['name'] as String,
        avgRating: (json['avgRating'] as num?)?.toDouble(),
        totalRatings: json['totalRatings'] as String?,
        deliveryTimeMinutes: json['deliveryTimeMinutes'] as int?,
        deliveryTimeRange: json['deliveryTimeRange'] as String?,
        costForTwo: json['costForTwo'] as String?,
        availabilityStatus: json['availabilityStatus'] as String?,
        nextOpenTime: json['nextOpenTime'] as String?,
        imageUrl: json['imageUrl'] as String?,
        cuisines: (json['cuisines'] as List<dynamic>?)
                ?.map((e) => e as String)
                .toList() ??
            [],
        areaName: json['areaName'] as String?,
        distanceKm: (json['distanceKm'] as num?)?.toDouble(),
        matchedPreferences: (json['matchedPreferences'] as List<dynamic>)
            .map((e) => e as String)
            .toList(),
        appDeepLink: json['appDeepLink'] as String,
        webUrl: json['webUrl'] as String,
        offer: json['offer'] as String?,
      );
}

class MatchResponse {
  final List<String> preferences;
  final int matchCount;
  final List<MatchedRestaurant> restaurants;

  const MatchResponse({
    required this.preferences,
    required this.matchCount,
    required this.restaurants,
  });

  factory MatchResponse.fromJson(Map<String, dynamic> json) => MatchResponse(
        preferences:
            (json['preferences'] as List<dynamic>).map((e) => e as String).toList(),
        matchCount: json['matchCount'] as int,
        restaurants: (json['restaurants'] as List<dynamic>)
            .map((e) => MatchedRestaurant.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
}
