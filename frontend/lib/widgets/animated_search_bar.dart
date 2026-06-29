import 'dart:async';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AnimatedSearchBar extends StatefulWidget {
  final VoidCallback onTap;
  const AnimatedSearchBar({super.key, required this.onTap});

  @override
  State<AnimatedSearchBar> createState() => _AnimatedSearchBarState();
}

class _AnimatedSearchBarState extends State<AnimatedSearchBar> {
  static const _words = [
    'shawarma',
    'biryani',
    'dal tadka',
    'pizza',
    'burger',
    'noodles',
    'paneer tikka',
    'sushi',
  ];

  int _i1 = 0;
  int _i2 = 3;
  Timer? _t1;
  Timer? _t2;

  @override
  void initState() {
    super.initState();
    _t1 = Timer.periodic(const Duration(milliseconds: 2500), (_) {
      if (mounted) setState(() => _i1 = (_i1 + 1) % _words.length);
    });
    // Offset word2 by 1.2 s so both words don't change simultaneously.
    Future.delayed(const Duration(milliseconds: 1200), () {
      if (!mounted) return;
      _t2 = Timer.periodic(const Duration(milliseconds: 2500), (_) {
        if (mounted) setState(() => _i2 = (_i2 + 1) % _words.length);
      });
    });
  }

  @override
  void dispose() {
    _t1?.cancel();
    _t2?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onTap,
      child: Container(
        height: 52,
        decoration: BoxDecoration(
          color: const Color(0xFFF5F5F5),
          borderRadius: BorderRadius.circular(12),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(
          children: [
            const Icon(Icons.search, color: Color(0xFF9B9B9B), size: 20),
            const SizedBox(width: 10),
            _RollingWord(word: _words[_i1]),
            Text(
              ' + ',
              style: GoogleFonts.poppins(
                color: const Color(0xFF9B9B9B),
                fontSize: 14,
              ),
            ),
            _RollingWord(word: _words[_i2]),
          ],
        ),
      ),
    );
  }
}

/// Displays a word that rolls: current exits upward + fades, next enters from
/// below + fades in. Width transitions are smoothed by [AnimatedSize].
class _RollingWord extends StatelessWidget {
  final String word;
  const _RollingWord({required this.word});

  @override
  Widget build(BuildContext context) {
    // AnimatedSize smoothly interpolates the widget's width as words change length.
    return AnimatedSize(
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
      child: AnimatedSwitcher(
        duration: const Duration(milliseconds: 280),
        // ClipRect prevents the sliding text from rendering outside the widget
        // bounds and overlapping adjacent widgets during transition.
        layoutBuilder: (currentChild, previousChildren) {
          return ClipRect(
            child: Stack(
              alignment: Alignment.centerLeft,
              children: <Widget>[
                ...previousChildren,
                ?currentChild,
              ],
            ),
          );
        },
        transitionBuilder: (child, animation) {
          // Compare the child's key to the CURRENT word to determine direction:
          // – incoming child (key == word): slides up from below
          // – outgoing child (key != word): exits upward
          final isEntering = child.key == ValueKey(word);

          final curve = CurvedAnimation(
            parent: animation,
            curve: isEntering ? Curves.easeOut : Curves.easeIn,
          );

          // SlideTransition uses fractional offsets relative to the child's own
          // height, so Offset(0, 1) == "one full text-line below".
          final offset = (isEntering
                  ? Tween<Offset>(begin: const Offset(0, 1), end: Offset.zero)
                  : Tween<Offset>(
                      begin: const Offset(0, -1), end: Offset.zero))
              .animate(curve);

          return FadeTransition(
            opacity: animation,
            child: SlideTransition(position: offset, child: child),
          );
        },
        child: Text(
          word,
          key: ValueKey(word),
          style: GoogleFonts.poppins(
            color: const Color(0xFF6B6B6B),
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
    );
  }
}
