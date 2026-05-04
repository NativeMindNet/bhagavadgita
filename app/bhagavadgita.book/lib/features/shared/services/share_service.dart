import 'package:share_plus/share_plus.dart';

class ShareService {
  final String _baseUrl = 'https://bhagavadgita.book';

  Future<void> shareVerse({required int chapter, required int verse}) async {
    final url = '$_baseUrl/?chapter=$chapter&verse=$verse';
    await SharePlus.instance.share('Check out this verse from the Bhagavad Gita: $url');
  }

  Future<void> shareChapter({required int chapter}) async {
    final url = '$_baseUrl/?chapter=$chapter';
    await SharePlus.instance.share('Read Chapter $chapter of the Bhagavad Gita: $url');
  }

  Future<void> shareCustom(String path, Map<String, String> queryParameters) async {
    final uri = Uri.parse('$_baseUrl$path').replace(queryParameters: queryParameters);
    await SharePlus.instance.share('Explore Bhagavad Gita: ${uri.toString()}');
  }
}
