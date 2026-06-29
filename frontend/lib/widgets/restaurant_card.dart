import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/restaurant.dart';

class RestaurantCard extends StatelessWidget {
  final MatchedRestaurant restaurant;
  const RestaurantCard({super.key, required this.restaurant});

  bool get _isClosed {
    final s = restaurant.availabilityStatus;
    return s != null && s.toUpperCase().contains('CLOSED');
  }

  // Raw number(s) only — used in the image overlay badge ("30-35", "30").
  String get _etaBadgeText {
    if (restaurant.deliveryTimeRange != null &&
        restaurant.deliveryTimeRange!.isNotEmpty) {
      return restaurant.deliveryTimeRange!
          .replaceAll(RegExp(r'\s*mins?.*', caseSensitive: false), '')
          .trim();
    }
    if (restaurant.deliveryTimeMinutes != null) {
      return '${restaurant.deliveryTimeMinutes}';
    }
    return '';
  }

  @override
  Widget build(BuildContext context) {
    final card = Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFF0F0F0)),
      ),
      clipBehavior: Clip.hardEdge,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildImage(),
          _buildContent(),
          if (_isClosed) _buildClosedBanner(),
        ],
      ),
    );

    return GestureDetector(
      onTap: _isClosed ? null : _openInSwiggy,
      child: _isClosed ? Opacity(opacity: 0.55, child: card) : card,
    );
  }

  Widget _buildImage() {
    final url = restaurant.imageUrl;
    final eta = _etaBadgeText;

    return AspectRatio(
      aspectRatio: 4 / 3,
      child: Stack(
        fit: StackFit.expand,
        children: [
          url != null && url.isNotEmpty
              ? CachedNetworkImage(
                  imageUrl: url,
                  fit: BoxFit.cover,
                  placeholder: (context, _) =>
                      Container(color: const Color(0xFFF5F5F5)),
                  errorWidget: (context, url, error) => _imagePlaceholder(),
                )
              : _imagePlaceholder(),
          if (eta.isNotEmpty)
            Positioned(
              bottom: 10,
              right: 10,
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.10),
                      blurRadius: 8,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      '$eta MINS',
                      style: GoogleFonts.poppins(
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                        color: const Color(0xFF1C1C1C),
                      ),
                    ),
                    Text(
                      'FREE DELIVERY',
                      style: GoogleFonts.poppins(
                        fontSize: 9,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFFFC8019),
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _imagePlaceholder() {
    return Container(
      color: const Color(0xFFF5F5F5),
      child: const Center(
        child: Icon(Icons.restaurant_outlined,
            color: Color(0xFFE0E0E0), size: 40),
      ),
    );
  }

  Widget _buildContent() {
    // Rating badge (green Swiggy-style)
    Widget? ratingBadge;
    if (restaurant.avgRating != null) {
      ratingBadge = Container(
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
        decoration: BoxDecoration(
          color: const Color(0xFF1BA672),
          borderRadius: BorderRadius.circular(6),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.star_rounded, color: Colors.white, size: 11),
            const SizedBox(width: 2),
            Text(
              restaurant.avgRating!.toStringAsFixed(1),
              style: GoogleFonts.poppins(
                fontSize: 11,
                fontWeight: FontWeight.w700,
                color: Colors.white,
              ),
            ),
          ],
        ),
      );
    }

    // Location line: area + distance
    final locationParts = <String>[
      if (restaurant.areaName?.isNotEmpty ?? false) restaurant.areaName!,
      if (restaurant.distanceKm != null)
        '${restaurant.distanceKm!.toStringAsFixed(1)} km',
    ];

    // Meta line: cuisines + cost
    final cuisines = restaurant.cuisines;
    final cuisineStr = cuisines.isEmpty
        ? null
        : cuisines.take(2).join(', ') + (cuisines.length > 2 ? '…' : '');
    final metaParts = [cuisineStr, restaurant.costForTwo]
        .whereType<String>()
        .toList();

    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            restaurant.name,
            style: GoogleFonts.poppins(
              fontSize: 18,
              fontWeight: FontWeight.w700,
              color: const Color(0xFF1C1C1C),
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              if (ratingBadge != null) ...[
                ratingBadge,
                const SizedBox(width: 6),
              ],
              if (restaurant.totalRatings != null) ...[
                Text(
                  '(${restaurant.totalRatings})',
                  style: GoogleFonts.poppins(
                      fontSize: 12, color: const Color(0xFF6B6B6B)),
                ),
                const SizedBox(width: 6),
              ],
              if (locationParts.isNotEmpty)
                Expanded(
                  child: Text(
                    locationParts.join(' · '),
                    style: GoogleFonts.poppins(
                        fontSize: 12, color: const Color(0xFF6B6B6B)),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
            ],
          ),
          if (metaParts.isNotEmpty) ...[
            const SizedBox(height: 3),
            Text(
              metaParts.join(' · '),
              style: GoogleFonts.poppins(
                  fontSize: 12, color: const Color(0xFF6B6B6B)),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildClosedBanner() {
    final openTime = restaurant.nextOpenTime;
    final label = (openTime != null && openTime.isNotEmpty)
        ? 'Closed · Opens at $openTime'
        : 'Currently unavailable';
    return Container(
      width: double.infinity,
      color: const Color(0xFFF0F0F0),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      child: Text(
        label,
        style: GoogleFonts.poppins(
          fontSize: 12,
          color: const Color(0xFF6B6B6B),
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }

  Future<void> _openInSwiggy() async {
    final deep = restaurant.appDeepLink;
    final web = restaurant.webUrl;
    if (deep.isNotEmpty) {
      final uri = Uri.parse(deep);
      if (await canLaunchUrl(uri)) {
        await launchUrl(uri);
        return;
      }
    }
    if (web.isNotEmpty) {
      await launchUrl(Uri.parse(web), mode: LaunchMode.externalApplication);
    }
  }
}
