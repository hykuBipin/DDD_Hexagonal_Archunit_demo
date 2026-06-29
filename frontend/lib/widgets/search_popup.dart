import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class SearchPopup extends StatefulWidget {
  final List<String>? initialPreferences;
  const SearchPopup({super.key, this.initialPreferences});

  @override
  State<SearchPopup> createState() => _SearchPopupState();
}

class _SearchPopupState extends State<SearchPopup> {
  final List<TextEditingController> _controllers = [];
  final List<FocusNode> _focusNodes = [];

  @override
  void initState() {
    super.initState();
    final initial = widget.initialPreferences;
    if (initial != null && initial.isNotEmpty) {
      for (final pref in initial) {
        _controllers.add(TextEditingController(text: pref));
        _focusNodes.add(FocusNode());
      }
    } else {
      _controllers.add(TextEditingController());
      _focusNodes.add(FocusNode());
    }
  }

  @override
  void dispose() {
    for (final c in _controllers) {
      c.dispose();
    }
    for (final f in _focusNodes) {
      f.dispose();
    }
    super.dispose();
  }

  bool get _canFind =>
      _controllers.any((c) => c.text.trim().isNotEmpty);

  bool get _allFieldsFilled =>
      _controllers.every((c) => c.text.trim().isNotEmpty);

  void _addField() {
    if (!_allFieldsFilled) return;
    final node = FocusNode();
    setState(() {
      _controllers.add(TextEditingController());
      _focusNodes.add(node);
    });
    Future.delayed(const Duration(milliseconds: 60), () {
      if (mounted) node.requestFocus();
    });
  }

  void _removeField(int index) {
    if (_controllers.length <= 1) return;
    final ctrl = _controllers[index];
    final node = _focusNodes[index];
    setState(() {
      _controllers.removeAt(index);
      _focusNodes.removeAt(index);
    });
    ctrl.dispose();
    node.dispose();
  }

  void _find() {
    final prefs = _controllers
        .map((c) => c.text.trim())
        .where((s) => s.isNotEmpty)
        .toList();
    if (prefs.isNotEmpty) Navigator.pop(context, prefs);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      child: Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: SafeArea(
          top: false,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  margin: const EdgeInsets.only(top: 12, bottom: 20),
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE0E0E0),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 0, 24, 0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "What's everyone craving?",
                      style: GoogleFonts.poppins(
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFF1C1C1C),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Add one dish per person',
                      style: GoogleFonts.poppins(
                        fontSize: 13,
                        color: const Color(0xFF6B6B6B),
                      ),
                    ),
                    const SizedBox(height: 20),
                    ...List.generate(
                      _controllers.length,
                      (i) => _buildField(i),
                    ),
                    const SizedBox(height: 4),
                    TextButton.icon(
                      onPressed: _allFieldsFilled ? _addField : null,
                      icon: Icon(
                        Icons.add_circle_outline,
                        color: _allFieldsFilled
                            ? const Color(0xFFFC8019)
                            : const Color(0xFFCCCCCC),
                        size: 20,
                      ),
                      label: Text(
                        'Add another craving',
                        style: GoogleFonts.poppins(
                          color: _allFieldsFilled
                              ? const Color(0xFFFC8019)
                              : const Color(0xFFCCCCCC),
                          fontWeight: FontWeight.w500,
                          fontSize: 14,
                        ),
                      ),
                      style: TextButton.styleFrom(padding: EdgeInsets.zero),
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: ElevatedButton(
                        onPressed: _canFind ? _find : null,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFFFC8019),
                          foregroundColor: Colors.white,
                          disabledBackgroundColor: const Color(0xFFE8E8E8),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(14),
                          ),
                          elevation: 0,
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.search, size: 18),
                            const SizedBox(width: 8),
                            Text(
                              'Find Restaurants',
                              style: GoogleFonts.poppins(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildField(int index) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controllers[index],
              focusNode: _focusNodes[index],
              onChanged: (_) => setState(() {}),
              textCapitalization: TextCapitalization.none,
              style: GoogleFonts.poppins(
                fontSize: 15,
                color: const Color(0xFF1C1C1C),
              ),
              decoration: InputDecoration(
                hintText: 'e.g. shawarma, biryani…',
                hintStyle: GoogleFonts.poppins(
                  color: const Color(0xFF9B9B9B),
                  fontSize: 14,
                ),
                filled: true,
                fillColor: const Color(0xFFF5F5F5),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(
                    color: Color(0xFFFC8019),
                    width: 1.5,
                  ),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 14,
                ),
              ),
            ),
          ),
          if (_controllers.length > 1) ...[
            const SizedBox(width: 8),
            GestureDetector(
              onTap: () => _removeField(index),
              child: Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  color: const Color(0xFFF5F5F5),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Icon(
                  Icons.close,
                  color: Color(0xFF9B9B9B),
                  size: 16,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
