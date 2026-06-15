# ============================================================
# config.py
# Konfigurasi global untuk Streamlit App
# Klasifikasi Kostum Tari Tradisional Jawa Tengah
# Fasya Maulinada - Universitas Muria Kudus
# ============================================================

# ─── INFORMASI KELAS ─────────────────────────────────────────
CLASS_NAMES = [
    'Tari_Bedhaya',
    'Tari_Dolalak',
    'Tari_Gambyong',
    'Tari_Golek',
    'Tari_Srimpi'
]

CLASS_DISPLAY_NAMES = [
    'Tari Bedhaya',
    'Tari Dolalak',
    'Tari Gambyong',
    'Tari Golek',
    'Tari Srimpi'
]

# ─── WARNA UNIK PER KELAS ────────────────────────────────────
CLASS_COLORS = {
    'Tari Bedhaya' : '#8B0000',  # Merah tua (sakral, keraton)
    'Tari Dolalak' : '#1A5276',  # Biru tua (militer, kolonial)
    'Tari Gambyong': '#B7950B',  # Emas/kuning (rakyat, ceria)
    'Tari Golek'   : '#1E8449',  # Hijau (remaja, segar)
    'Tari Srimpi'  : '#6C3483',  # Ungu (keanggunan, halus)
}

CLASS_EMOJIS = {
    'Tari Bedhaya' : '🏛️',
    'Tari Dolalak' : '💂',
    'Tari Gambyong': '🌟',
    'Tari Golek'   : '🌸',
    'Tari Srimpi'  : '🦋',
}

# ─── DESKRIPSI LENGKAP SETIAP TARIAN ────────────────────────
DANCE_INFO = {
    'Tari Bedhaya': {
        'asal'          : 'Keraton Surakarta & Yogyakarta, Jawa Tengah',
        'era'           : 'Abad ke-17 (Zaman Mataram Islam)',
        'penari'        : '7 atau 9 penari putri',
        'fungsi'        : 'Tarian sakral keraton, upacara adat',
        'deskripsi'     : (
            'Tari Bedhaya adalah tarian sakral dan tertua dari keraton Jawa yang '
            'mencerminkan kerumitan budaya keraton Surakarta dan Yogyakarta. '
            'Tarian ini memiliki nilai-nilai religius yang mendalam dan melambangkan '
            'hubungan manusia dengan Tuhan. Gerakan tarian ini sangat halus, '
            'terstruktur, dan penuh makna filosofis.'
        ),
        'kostum'        : (
            'Kostum Tari Bedhaya menggunakan kain batik bermotif khusus keraton '
            '(seperti motif Parang Rusak atau Sido Asih) dengan warna dominan '
            'kuning keemasan dan hitam. Dilengkapi dengan kemben (penutup dada), '
            'sampur (selendang), cundhuk mentul (hiasan kepala bunga emas), '
            'kalung susun, gelang, dan aksesoris emas lainnya yang sangat detail.'
        ),
        'keunikan'      : [
            'Tarian sakral yang hanya ditampilkan pada upacara khusus keraton',
            'Gerakannya sangat halus dan bermakna filosofis mendalam',
            'Ditarikan oleh 7 (Bedhaya Ketawang) atau 9 penari sekaligus',
            'Kostum menggunakan batik bermotif eksklusif keraton',
            'Diiringi gamelan dengan gending khusus Ketawang'
        ],
        'nilai_filosofis': 'Melambangkan hubungan antara manusia (mikrokosmos) dengan Tuhan (makrokosmos)',
    },

    'Tari Dolalak': {
        'asal'          : 'Kabupaten Purworejo, Jawa Tengah',
        'era'           : 'Awal abad ke-20 (Masa penjajahan Belanda)',
        'penari'        : 'Berkelompok (awalnya pria, kini banyak perempuan)',
        'fungsi'        : 'Hiburan rakyat, festival budaya',
        'deskripsi'     : (
            'Tari Dolalak merupakan warisan budaya dari zaman penjajahan Belanda '
            'yang merupakan hasil akulturasi budaya Barat dan Jawa. Tarian ini '
            'meniru gerak-gerik serdadu Belanda yang sedang berpesta, dengan iringan '
            'musik tradisional. Memiliki keunikan pada gerak dansa dan rampak barisan '
            'yang energik dan dinamis.'
        ),
        'kostum'        : (
            'Kostum Tari Dolalak terinspirasi dari seragam serdadu Belanda (militer). '
            'Menggunakan baju lengan panjang berwarna hitam atau gelap dengan ornamen '
            'bintang/pangkat di bahu, celana panjang, topi pet (mirip topi militer), '
            'kacamata hitam, dan kain sarung yang dililitkan di pinggang. '
            'Terdapat aksesoris payet yang berkilau pada bagian baju.'
        ),
        'keunikan'      : [
            'Hasil akulturasi budaya Barat (Belanda) dan Jawa yang unik',
            'Gerakan meniru serdadu Belanda yang berpesta',
            'Dilengkapi aksi "ndadi" (kesurupan) pada pertunjukan tradisional',
            'Kostum terinspirasi seragam militer kolonial Belanda',
            'Sangat populer di Kabupaten Purworejo hingga tersebar di setiap kecamatan'
        ],
        'nilai_filosofis': 'Simbol perlawanan budaya Jawa terhadap kolonialisme melalui seni',
    },

    'Tari Gambyong': {
        'asal'          : 'Surakarta (Solo), Jawa Tengah',
        'era'           : 'Abad ke-19 (Berkembang dari Tayub/Tledhek)',
        'penari'        : 'Tunggal putri atau berkelompok',
        'fungsi'        : 'Penyambutan tamu, pembukaan acara, pertunjukan seni',
        'deskripsi'     : (
            'Tari Gambyong awalnya merupakan tari tunggal putri dari kalangan rakyat '
            '(tledhek), namun kini sering ditarikan berkelompok untuk berbagai keperluan. '
            'Tarian ini mencerminkan kecantikan, kelembutan, dan keanggunan wanita Jawa. '
            'Gerakan tangan (sabetan) dan pinggul yang khas menjadi ciri utamanya.'
        ),
        'kostum'        : (
            'Kostum Tari Gambyong menggunakan kebaya panjang bermotif bunga atau batik '
            'dengan warna cerah (merah, hijau, atau kuning). Dilengkapi dengan jarik '
            '(kain batik) yang dililitkan, sampur (selendang) yang digunakan dalam '
            'gerakan tari, sanggul rambut dengan melati atau bunga, '
            'kalung, gelang, dan anting tradisional Jawa.'
        ),
        'keunikan'      : [
            'Berakar dari tarian rakyat (tledhek) yang kemudian masuk keraton',
            'Gerakan tangan (sabetan) yang sangat ekspresif dan khas',
            'Kostum dapat bervariasi sesuai permintaan (fleksibel)',
            'Sering digunakan sebagai tarian pembuka berbagai acara formal',
            'Diiringi gamelan dengan gending Gambyong yang khas'
        ],
        'nilai_filosofis': 'Melambangkan kecantikan dan keluwesan perempuan Jawa yang berbudi pekerti luhur',
    },

    'Tari Golek': {
        'asal'          : 'Yogyakarta & Surakarta, Jawa Tengah',
        'era'           : 'Abad ke-19 (Masa Kerajaan Mataram)',
        'penari'        : 'Tunggal putri',
        'fungsi'        : 'Pertunjukan seni, pelestarian budaya',
        'deskripsi'     : (
            'Tari Golek merupakan tarian klasik Jawa yang sangat populer, '
            'merepresentasikan seorang remaja putri yang sedang dalam masa pencarian '
            'jati diri melalui upaya berhias (bersolek). Kata "golek" dalam bahasa '
            'Jawa berarti "mencari". Tarian ini menggambarkan proses seorang gadis '
            'yang sedang berdandan dan mempersiapkan diri.'
        ),
        'kostum'        : (
            'Kostum Tari Golek sangat lengkap dan colorful, mencerminkan gadis yang '
            'sedang berhias. Menggunakan kebaya atau kemben bermotif dengan warna '
            'cerah dan mencolok, dilengkapi banyak aksesoris: cundhuk mentul, '
            'kalung bertingkat, gelang kaki (binggel), sampur warna-warni, '
            'dan seluruh kostum dihiasi payet berkilau yang menggambarkan kemewahan '
            'dan kecantikan seorang gadis.'
        ),
        'keunikan'      : [
            'Menggambarkan proses berhias seorang remaja putri secara simbolis dalam gerakan',
            'Kostum paling "penuh aksesoris" dibanding tarian Jawa lainnya',
            'Gerakan tari sangat detail, mencerminkan setiap tahap berdandan',
            'Diiringi gending khusus yang berirama lembut namun ceria',
            'Populer sebagai materi pembelajaran tari Jawa klasik'
        ],
        'nilai_filosofis': 'Proses pencarian identitas dan kematangan seorang gadis menjadi wanita dewasa',
    },

    'Tari Srimpi': {
        'asal'          : 'Keraton Surakarta & Yogyakarta, Jawa Tengah',
        'era'           : 'Abad ke-17 (Setara usia dengan Bedhaya)',
        'penari'        : '4 penari putri (melambangkan 4 elemen)',
        'fungsi'        : 'Penyambutan tamu kehormatan, upacara keraton',
        'deskripsi'     : (
            'Tari Srimpi merupakan tarian putri keraton yang berkarakter lungguh '
            '(halus, anggun) dan ditarikan secara berkelompok oleh 4 orang penari. '
            'Keempat penari melambangkan 4 elemen alam: air, api, angin, dan bumi. '
            'Tarian ini sering digunakan untuk menyambut tamu kehormatan dan '
            'mencerminkan keagungan budaya keraton Jawa.'
        ),
        'kostum'        : (
            'Kostum Tari Srimpi hampir serupa dengan Bedhaya namun dengan variasi '
            'warna yang berbeda. Menggunakan kain batik keraton bermotif khusus, '
            'kemben (penutup dada), dengan warna dominan kuning gading, hijau, '
            'atau biru tua. Dilengkapi dengan cundhuk mentul (hiasan kepala), '
            'kalung, gelang, sampur sutra halus, dan aksesoris emas yang melambangkan '
            'keanggunan dan kehalusan budi pekerti wanita keraton.'
        ),
        'keunikan'      : [
            'Ditarikan tepat oleh 4 penari, melambangkan 4 elemen alam semesta',
            'Gerakan sangat sinkron dan presisi antar 4 penari',
            'Kostum dan makeup sangat identik di antara 4 penari',
            'Merupakan simbol keanggunan dan kehalusan budaya keraton',
            'Hanya ditampilkan pada acara-acara penting dan resmi keraton'
        ],
        'nilai_filosofis': 'Keselarasan dan keseimbangan 4 elemen alam yang menciptakan harmoni kehidupan',
    }
}

# ─── KONFIGURASI MODEL ────────────────────────────────────────
IMG_SIZE        = (224, 224)
MODEL_FILE      = 'model_kostum_tari.keras'
MODEL_FILE_H5   = 'model_kostum_tari.h5'
METADATA_FILE   = 'model_metadata.json'
CLASS_IDX_FILE  = 'class_indices.json'

# ─── THRESHOLD CONFIDENCE ─────────────────────────────────────
CONFIDENCE_HIGH   = 0.85   # ≥ 85%: sangat yakin
CONFIDENCE_MEDIUM = 0.65   # 65-85%: cukup yakin
CONFIDENCE_LOW    = 0.00   # < 65%: kurang yakin

# ─── INFORMASI APLIKASI ──────────────────────────────────────
APP_TITLE    = 'TariKenali'
APP_SUBTITLE = 'Klasifikasi Kostum Tari Tradisional Jawa Tengah'
APP_VERSION  = '1.0.0'
RESEARCHER   = 'Fasya Maulinada'
NIM          = '202251155'
UNIVERSITY   = 'Universitas Muria Kudus'
SUPERVISOR_1 = 'Dr. Ahmad Abdul Chamid, S.Kom., M.Kom.'
SUPERVISOR_2 = 'Dr. Ahmad Jazuli, S.Kom., M.Kom.'
YEAR         = '2025'
