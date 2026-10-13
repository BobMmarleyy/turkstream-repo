# TurkStream Repo

Bu repo, Cloudstream için Türkçe film/dizi eklentileri ve canlı TV/IPTV kaynaklarını yöneten bir depo sistemi içerir.

## Kurulum

1. Cloudstream uygulamasını açın
2. Ayarlar → Eklentiler → Depo ekle
3. Aşağıdaki URL'yi girin:
   ```
   https://raw.githubusercontent.com/BobMmarleyy/turkstream-repo/main/repo.json
   ```

## Yapılandırma

- `repo.json`: Cloudstream ile uyumlu depo tanımı
- `sources.json`: Kontrol edilecek kaynakların yapılandırması
- `monitor.py`: Kaynak erişilebilirliği, hata ve değişiklik kontrolleri

## Testler

- `tests/` dizini altında otomatik testler bulunur