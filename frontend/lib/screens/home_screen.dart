import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../models/address.dart';
import 'location_screen.dart';
import 'results_screen.dart';
import '../widgets/animated_search_bar.dart';
import '../widgets/search_popup.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Address? _selectedAddress;

  // (image1, image2, dish1, dish2)
  static const List<(String, String, String, String)> _combos = [
    ('assets/images/shawarma.jpg', 'assets/images/biriyani.avif', 'shawarma', 'biryani'),
    ('assets/images/pizza.jpg', 'assets/images/pasta.jpg', 'pizza', 'pasta'),
    ('assets/images/dal_tadka.jpeg', 'assets/images/naan.jpg', 'dal tadka', 'naan'),
    ('assets/images/burger.jpeg', 'assets/images/milkshake.jpeg', 'burger', 'milkshake'),
    ('assets/images/sushi.webp', 'assets/images/ramen.jpg', 'sushi', 'ramen'),
    ('assets/images/paneer_tikka.webp', 'assets/images/butter_naan.jpg', 'paneer tikka', 'butter naan'),
  ];

  Future<void> _openLocationPicker() async {
    final address = await Navigator.push<Address>(
      context,
      MaterialPageRoute(builder: (_) => const LocationScreen()),
    );
    if (address != null && mounted) {
      setState(() => _selectedAddress = address);
    }
  }

  Future<void> _openSearchPopup({List<String>? initial}) async {
    if (_selectedAddress == null) {
      await _openLocationPicker();
      if (_selectedAddress == null) return;
    }
    if (!mounted) return;
    final prefs = await showModalBottomSheet<List<String>>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => SearchPopup(initialPreferences: initial),
    );
    if (prefs != null && prefs.isNotEmpty && mounted) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ResultsScreen(
            preferences: prefs,
            addressId: _selectedAddress?.id,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 24, 20, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildAddressHeader(),
                  const SizedBox(height: 22),
                  AnimatedSearchBar(onTap: () => _openSearchPopup()),
                  const SizedBox(height: 28),
                  _buildSectionHeader(),
                  const SizedBox(height: 14),
                ],
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
                child: LayoutBuilder(
                  builder: (context, constraints) {
                    const cols = 2;
                    const rows = 3;
                    const spacing = 12.0;
                    final tileH =
                        (constraints.maxHeight - (rows - 1) * spacing) / rows;
                    final tileW =
                        (constraints.maxWidth - (cols - 1) * spacing) / cols;
                    return GridView.builder(
                      physics: const NeverScrollableScrollPhysics(),
                      gridDelegate:
                          SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: cols,
                        crossAxisSpacing: spacing,
                        mainAxisSpacing: spacing,
                        childAspectRatio: tileW / tileH,
                      ),
                      itemCount: _combos.length,
                      itemBuilder: (context, index) =>
                          _buildComboTile(_combos[index]),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAddressHeader() {
    final addr = _selectedAddress;
    return GestureDetector(
      onTap: _openLocationPicker,
      behavior: HitTestBehavior.opaque,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(top: 2),
            child: Icon(Icons.location_on, color: Color(0xFFFC8019), size: 22),
          ),
          const SizedBox(width: 6),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      addr != null
                          ? (addr.addressTag ??
                              addr.addressCategory ??
                              'Location')
                          : 'Set delivery address',
                      style: GoogleFonts.poppins(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: addr != null
                            ? const Color(0xFF1C1C1C)
                            : const Color(0xFFFC8019),
                      ),
                    ),
                    const SizedBox(width: 4),
                    Icon(
                      Icons.keyboard_arrow_down_rounded,
                      size: 20,
                      color: addr != null
                          ? const Color(0xFF1C1C1C)
                          : const Color(0xFFFC8019),
                    ),
                  ],
                ),
                if (addr != null) ...[
                  const SizedBox(height: 1),
                  Text(
                    addr.addressLine,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: GoogleFonts.poppins(
                      fontSize: 12,
                      color: const Color(0xFF6B6B6B),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.baseline,
      textBaseline: TextBaseline.alphabetic,
      children: [
        Text(
          'Popular combos',
          style: GoogleFonts.poppins(
            fontSize: 17,
            fontWeight: FontWeight.w600,
            color: const Color(0xFF1C1C1C),
          ),
        ),
        Text(
          'Tap to search →',
          style: GoogleFonts.poppins(
            fontSize: 12,
            color: const Color(0xFF9B9B9B),
          ),
        ),
      ],
    );
  }

  Widget _buildComboTile((String, String, String, String) combo) {
    return _SplitComboTile(
      image1: combo.$1,
      image2: combo.$2,
      dish1: combo.$3,
      dish2: combo.$4,
      onTap: () => _openSearchPopup(initial: [combo.$3, combo.$4]),
    );
  }
}

// ── Diagonal split tile ────────────────────────────────────────────────────

class _SplitComboTile extends StatelessWidget {
  final String image1;
  final String image2;
  final String dish1;
  final String dish2;
  final VoidCallback onTap;

  const _SplitComboTile({
    required this.image1,
    required this.image2,
    required this.dish1,
    required this.dish2,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: const Color(0xFF2A2A2A),
          borderRadius: BorderRadius.circular(16),
          boxShadow: const [
            BoxShadow(
              color: Color(0x28000000),
              blurRadius: 12,
              offset: Offset(0, 4),
            ),
          ],
        ),
        clipBehavior: Clip.hardEdge,
        child: Stack(
          fit: StackFit.expand,
          children: [
            // Left dish image (full background)
            Image.asset(
              image1,
              fit: BoxFit.cover,
              frameBuilder: _fadeInFrame,
              errorBuilder: (context, error, stackTrace) =>
                  Container(color: const Color(0xFFE0E0E0)),
            ),
            // Right dish image — clipped to the diagonal half
            ClipPath(
              clipper: const _DiagonalClipper(),
              child: Image.asset(
                image2,
                fit: BoxFit.cover,
                frameBuilder: _fadeInFrame,
                errorBuilder: (context, error, stackTrace) =>
                    Container(color: const Color(0xFFCCCCCC)),
              ),
            ),
            // White diagonal separator line
            CustomPaint(painter: const _DiagonalLinePainter()),
            // Dark gradient + labels at the bottom
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Color(0x00000000), Color(0xCC000000)],
                  ),
                ),
                padding: const EdgeInsets.fromLTRB(12, 28, 12, 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      dish1,
                      style: GoogleFonts.poppins(
                        color: Colors.white,
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      '+ $dish2',
                      style: GoogleFonts.poppins(
                        color: const Color(0xCCFFFFFF),
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// Shared frameBuilder that fades images in when they finish decoding.
// Skips the animation when the image was already in cache (synchronous load).
Widget _fadeInFrame(
    BuildContext context, Widget child, int? frame, bool wasSynchronouslyLoaded) {
  if (wasSynchronouslyLoaded) return child;
  return AnimatedOpacity(
    opacity: frame == null ? 0.0 : 1.0,
    duration: const Duration(milliseconds: 350),
    curve: Curves.easeIn,
    child: child,
  );
}

// Clips the right half of the tile along a diagonal line.
// Top cut at 53% from left, bottom cut at 40% from left.
class _DiagonalClipper extends CustomClipper<Path> {
  const _DiagonalClipper();

  @override
  Path getClip(Size size) {
    return Path()
      ..moveTo(size.width * 0.53, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width, size.height)
      ..lineTo(size.width * 0.40, size.height)
      ..close();
  }

  @override
  bool shouldReclip(covariant CustomClipper<Path> oldClipper) => false;
}

// Draws the white separator line along the diagonal.
class _DiagonalLinePainter extends CustomPainter {
  const _DiagonalLinePainter();

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawLine(
      Offset(size.width * 0.53, 0),
      Offset(size.width * 0.40, size.height),
      Paint()
        ..color = const Color(0xDDFFFFFF)
        ..strokeWidth = 1.5,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
