import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../models/restaurant.dart';
import '../services/api_service.dart';
import '../widgets/restaurant_card.dart';

class ResultsScreen extends StatefulWidget {
  final List<String> preferences;
  final String? addressId;

  const ResultsScreen({
    super.key,
    required this.preferences,
    this.addressId,
  });

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  MatchResponse? _response;
  String? _error;
  bool _loading = true;
  bool _showBanner = false;
  int _visibleCount = 0;

  @override
  void initState() {
    super.initState();
    _loadResults();
  }

  Future<void> _loadResults() async {
    setState(() {
      _loading = true;
      _error = null;
      _showBanner = false;
      _visibleCount = 0;
    });
    try {
      final response = await ApiService.matchRestaurants(
        widget.preferences,
        widget.addressId ?? '',
      );
      if (!mounted) return;
      setState(() {
        _response = response;
        _loading = false;
      });
      // Animate the match banner in on the next frame.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) setState(() => _showBanner = true);
      });
      // Stagger cards in.
      for (int i = 0; i < response.restaurants.length; i++) {
        await Future.delayed(const Duration(milliseconds: 80));
        if (!mounted) break;
        setState(() => _visibleCount = i + 1);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = e.toString();
          _loading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        scrolledUnderElevation: 0,
        leading: IconButton(
          icon: const Icon(
            Icons.arrow_back_ios_new,
            color: Color(0xFF1C1C1C),
            size: 20,
          ),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'OrderTogether',
          style: GoogleFonts.poppins(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: const Color(0xFF1C1C1C),
          ),
        ),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_loading) return _buildLoading();
    if (_error != null) return _buildError();
    final resp = _response;
    if (resp == null) return const SizedBox.shrink();
    if (resp.restaurants.isEmpty) return _buildEmpty();
    return _buildResults(resp);
  }

  Widget _buildLoading() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(
            width: 40,
            height: 40,
            child: CircularProgressIndicator(
              color: Color(0xFFFC8019),
              strokeWidth: 3,
            ),
          ),
          const SizedBox(height: 16),
          Text(
            'Checking menus…',
            style: GoogleFonts.poppins(
              color: const Color(0xFF6B6B6B),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            widget.preferences.join(' + '),
            style: GoogleFonts.poppins(
              color: const Color(0xFFFC8019),
              fontSize: 13,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.wifi_off_outlined,
              size: 56,
              color: Color(0xFF9B9B9B),
            ),
            const SizedBox(height: 16),
            Text(
              'Something went wrong',
              style: GoogleFonts.poppins(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: const Color(0xFF1C1C1C),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Check your connection and try again',
              textAlign: TextAlign.center,
              style: GoogleFonts.poppins(
                fontSize: 13,
                color: const Color(0xFF6B6B6B),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _loadResults,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFFC8019),
                foregroundColor: Colors.white,
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                  vertical: 14,
                ),
              ),
              child: Text(
                'Try Again',
                style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmpty() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.search_off_rounded,
              size: 64,
              color: Color(0xFFFC8019),
            ),
            const SizedBox(height: 16),
            Text(
              'No matches found',
              style: GoogleFonts.poppins(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: const Color(0xFF1C1C1C),
              ),
            ),
            const SizedBox(height: 10),
            Text(
              'No restaurant nearby serves all of:\n${widget.preferences.join(' + ')}',
              textAlign: TextAlign.center,
              style: GoogleFonts.poppins(
                fontSize: 13,
                color: const Color(0xFF6B6B6B),
                height: 1.5,
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFFC8019),
                foregroundColor: Colors.white,
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                padding: const EdgeInsets.symmetric(
                  horizontal: 32,
                  vertical: 14,
                ),
              ),
              child: Text(
                'Try different cravings',
                style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResults(MatchResponse resp) {
    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
      itemCount: resp.restaurants.length + 1,
      itemBuilder: (context, index) {
        if (index == 0) return _buildMatchBanner(resp);
        final i = index - 1;
        final visible = i < _visibleCount;
        return AnimatedOpacity(
          opacity: visible ? 1.0 : 0.0,
          duration: const Duration(milliseconds: 400),
          curve: Curves.easeOut,
          child: AnimatedSlide(
            offset: visible ? Offset.zero : const Offset(0, 0.06),
            duration: const Duration(milliseconds: 400),
            curve: Curves.easeOutCubic,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: RestaurantCard(restaurant: resp.restaurants[i]),
            ),
          ),
        );
      },
    );
  }

  Widget _buildMatchBanner(MatchResponse resp) {
    final count = resp.matchCount;
    final label = widget.preferences.join(' + ');
    return AnimatedScale(
      scale: _showBanner ? 1.0 : 0.85,
      duration: const Duration(milliseconds: 500),
      curve: Curves.elasticOut,
      child: AnimatedOpacity(
        opacity: _showBanner ? 1.0 : 0.0,
        duration: const Duration(milliseconds: 280),
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 16),
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: const Color(0xFFFFF3E8),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: const Color(0xFFFFD4A3)),
          ),
          child: Row(
            children: [
              Container(
                width: 42,
                height: 42,
                decoration: BoxDecoration(
                  color: const Color(0xFF2ECC71),
                  borderRadius: BorderRadius.circular(21),
                ),
                child: const Icon(Icons.check_rounded, color: Colors.white, size: 24),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$count ${count == 1 ? 'restaurant' : 'restaurants'} found',
                      style: GoogleFonts.poppins(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFF1C1C1C),
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      'Serving $label',
                      style: GoogleFonts.poppins(
                        fontSize: 13,
                        color: const Color(0xFF6B6B6B),
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
