curl 'https://applets.ebxcdn.com/applets/www.detik.com/scripts.js' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://www.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0'


!function(){const r="ebx_webtag_",n="utm_source",w="QUERY",d="FRAGMENT",l=Date.now();function f(){var t=document.body||{},n=document.documentElement||{};return Math.max(t.scrollHeight||0,t.offsetHeight||0,t.clientHeight||0,n.scrollHeight||0,n.offsetHeight||0,n.clientHeight||0)}function p(t){var n;navigator.sendBeacon?navigator.sendBeacon(t):((n=new XMLHttpRequest).open("POST",t,!1),n.setRequestHeader("Content-Type","application/x-www-form-urlencoded"),n.send())}function e(t){let n="";var e={};return t.search&&""!==(n=o(t.search.replace("?","")))&&(e.location=w),""===n&&t.hash&&""!==(n=o(t.hash.replace("#","")))&&(e.location=d),""===n?null:(e.source=n,e)}function o(t){t=t.split("&").filter(t=>{return t.split("=")[0]===n});return 0<t.length?t[0]:""}function c(n,e,o){if(window.sessionStorage){let t=n;n?(t.referrer=e,t.utmSource=o):t={referrer:e,utmSource:o},window.sessionStorage.setItem(r,JSON.stringify(t))}}try{let t=window.location,n=document.referrer,i=70;window.location.pathname&&0!==window.location.pathname.length&&"/"!==window.location.pathname||(i=97);try{var a,u,m=function(){{var t;if(window.sessionStorage)return t=window.sessionStorage.getItem(r),JSON.parse(t)}return null}();m?""!==n&&new URL(n).host===t.host?(n=m.referrer,m.utmSource&&(t=function(t,n){var e=n.location,n=n.source,o=t.protocol,r=t.host,c=t.pathname;let a=t.search,u=t.hash;e===w?a+=(""===a?"?":"")+n:e===d&&(u+=(""===u?"#":"")+n);return o+"//"+r+c+a+u}(t,m.utmSource))):(a=e(t),c(m,n,a)):(u=e(t),c(m,n,u))}catch(t){}const v=encodeURIComponent(t),s=encodeURIComponent(n);if(100*Math.random()>=i){const $='urn:traffic:applet:faggokfq';let u;try{u=Intl.DateTimeFormat().resolvedOptions().timeZone}catch(t){u=""}p(`https://trackerapi.ebxcdn.com/v1/track?r=${s}&l=${v}&sp=${i}&u=${$}&tz=`+u),window.addEventListener("beforeunload",()=>{var t=s,n=v,e=i,o=$,r=u;try{var c=Math.round(function(){var t=f(),n=document.body||{},e=document.documentElement||{},o=window.innerHeight||e.clientHeight||0,e=window.scrollY||e.scrollTop||n.scrollTop||0;return t<=o?t:e+o}()/f()*100),a=Date.now()-l;p(`https://trackerapi.ebxcdn.com/v1/track/engagement?r=${t}&l=${n}&sp=${e}&u=${o}&tz=${r}&sd=${c}&dt=`+a)}catch(t){console.log("Failed to track engagement")}})}}catch(t){console.log("Failed to track page view")}}();

curl 'https://www.google.com/ccm/collect?frm=0&ae=g&en=page_view&dl=https%3A%2F%2Fwww.detik.com%2F&scrsrc=www.googletagmanager.com&rnd=709169925.1774261922&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&auid=997881967.1774261778&navt=r&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115616986~115938466~115938469~116024733~117484252~118131589&apve=1&apvf=f&apvc=1&tft=1774261922007&tfd=5935' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://www.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0'
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261921756&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=0&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115616986~115938466~115938469~116024733~117484252~118104772&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fwww.detik.com%2F&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&en=page_view&tfd=6185' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE='


{
    "head": {
        "timestamp": 1774261947,
        "type": "ChannelsKeywordsNoCache",
        "version": "1.0.1-model-b"
    },
    "body": [
        {
            "id": "260323129",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/4700c050520240a7be1d9502ee7fa0ea-20260323155745-0s.webp?a=1",
            "description": "\"Hei, Trump, kau dipecat! Kau sudah familiar dengan kalimat ini,\" adalah kalimat ledekan dari juru bicara militer Iran dari Markas Besar Pusat Khatam al-Anbiya, Ebrahim Zolfaghari. 'Kau dipecat' memang identik dengan Presiden Amerika Serikat (AS) Donald Trump. Kata itu diucapkan Trump dalam reality show 'The Apprentice' di akhir setiap episode. Inti dari acara ini adalah kompetisi dalam tugas-tugas bisnis. Cuma yang kuat yang bertahan. Para pesaing terlemah bakal diberitahu kekurangan mereka secara langsung dan langsung dipecat Trump dengan kalimat khas 'Kau dipecat!'. Sementara Ebrahim Zolfaghari memakai kata 'Trump, kau dipecat!' sebagai penutup dalam pernyataan pers terbarunya. \"Musuh memaksa mereka yang lebih memilih melarikan diri daripada bertahan, penguasa kekalahan beruntun yang sama yang menggunakan umat Muslim di wilayah ini sebagai perisai manusia mereka,\" ujar Ebrahim. \"Hingga saat serangan kita tiba, sehingga mereka dapat terbebas dari rasa takut bahkan sebelum dampaknya terjadi dan ini adalah balasan yang setimpal bagi setiap musuh yang menaruh niat jahat terhadap keamanan rakyat kami,\" tambahnya.",
            "duration": 60,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/4700c050520240a7be1d9502ee7fa0ea-20260323155824-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 16:01:10",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/4700c050520240a7be1d9502ee7fa0ea.smil/playlist.m3u8",
            "tag": "donald trump,trump,iran,ebrahim zolfaghari,the apprentice",
            "title": "Video Asal-usul Ledekan 'Trump, Kau Dipecat!' dari Jubir Militer Iran",
            "unixtime": 1774256470000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323129/video-asalusul-ledekan-trump-kau-dipecat-dari-jubir-militer-iran"
        },
        {
            "id": "260323004",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/d78f1427aef64e0d85eaae7a3fee06ad-20260323071538-0s.webp?a=1",
            "description": "Presiden Republik Indonesia, Prabowo Subianto, menegaskan rencana besar pemerintah untuk melakukan konversi massal kendaraan bermesin bensin ke tenaga listrik. Langkah ini disebutnya sebagai strategi utama (game changer) untuk memperkuat ekonomi masyarakat dan mengurangi ketergantungan pada bahan bakar fosil.",
            "duration": 67,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://akcdn.detik.net.id/community/media/visual/2026/03/23/prabowo-semua-mobil-motor-pakai-listrik-orang-kaya-silakan-isi-bensin-1774225098670_916.jpeg?w=620",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 07:19:14",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/d78f1427aef64e0d85eaae7a3fee06ad.smil/playlist.m3u8",
            "tag": "prabowo,mobil listrik",
            "title": "Prabowo: Semua Mobil-motor Pakai Listrik, Orang Kaya Silakan Isi Bensin",
            "unixtime": 1774225154000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323004/prabowo-semua-mobilmotor-pakai-listrik-orang-kaya-silakan-isi-bensin"
},
        {
            "id": "260323018",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/16dc31ee1cce47d0b0099b58cee3c958-20260323123202-0s.webp?a=1",
            "description": "Perdana Menteri Israel Benjamin Netanyahu mengunjungi Kota Arad dan Dimona yang porak poranda setelah menjadi sasaran misil Iran. Netanyahu mengatakan apa yang dilakukan Iran adalah bukti bahwa mereka berbahaya bagi seluruh dunia.",
            "duration": 85,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/16dc31ee1cce47d0b0099b58cee3c958-20260323123233-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 12:58:50",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/16dc31ee1cce47d0b0099b58cee3c958.smil/playlist.m3u8",
            "tag": "benjamin netanyahu,perdana menteri israel benjamin netanyahu,israel,perang israel-as vs iran,netanyahu",
            "title": "Video Netanyahu Setelah Israel Digempur: Iran Ancaman Bagi Seluruh Dunia",
            "unixtime": 1774245530000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323018/video-netanyahu-setelah-israel-digempur-iran-ancaman-bagi-seluruh-dunia"
        },
        {
            "id": "260323114",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/604b465532b8427aa781388e579e8511-20260323152634-0s.webp?a=1",
            "description": "Kapolda Jawa Barat Irjen Pol Rudi Setiawan memantau kondisi arus lalu lintas di Jalan Raya Simpang Gadog, Bogor, Jawa Barat, Senin (23/3). Dia menyorot banyaknya pungli yang kerap terjadi di tempat-tempat wisata saat masa libur Lebaran. Terkait ini, Rudi menjamin tidak boleh ada pungli kepada wisatawan di seluruh destinasi wisata se-Jawa Barat.",
            "duration": 42,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/604b465532b8427aa781388e579e8511-20260323152619-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 15:56:10",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/604b465532b8427aa781388e579e8511.smil/playlist.m3u8",
            "tag": "kapolda jawa barat,irjen pol rudi setiawan,simpang gadog,pungli,tempat wisata puncak bogor,lebaran,lebaran 2026",
            "title": "Video Kapolda Jabar Pastikan Tak Ada Pungli di Tempat Wisata se-Jawa Barat",
            "unixtime": 1774256170000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323114/video-kapolda-jabar-pastikan-tak-ada-pungli-di-tempat-wisata-sejawa-barat"
        },
        {
            "id": "260323017",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/7bea186779fb4e6cba5b02760ddb75b4-20260323115321-0s.webp?a=1",
            "description": "Kawasan Stadion Utama Gelora Bung Karno (SUBGBK) jadi tempat favorit bagi warga untuk berolahraga di hari ketiga Lebaran 2026. Seperti pemain Persib Bandung dan eks kiper Timnas Indonesia, I Made Wirawan, yang menghabiskan hari ketiga Lebaran dengan berolahraga bersama keluarga di GBK. Ia memilih GBK karena nyaman untuk jogging dan memiliki suasana asri dengan banyak pepohonan. Menurutnya, kegiatan ini juga menjadi momen pas untuk berekreasi bersama keluarga.",
            "duration": 77,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/7bea186779fb4e6cba5b02760ddb75b4-20260323115249-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 13:14:46",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/7bea186779fb4e6cba5b02760ddb75b4.smil/playlist.m3u8",
            "tag": "i made wirawan,gbk,jakarta",
            "title": "Video: I Made Wirawan Pilih Berolahraga di GBK di Hari Ketiga Lebaran",
            "unixtime": 1774246486000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323017/video-i-made-wirawan-pilih-berolahraga-di-gbk-di-hari-ketiga-lebaran"
        },
        {
            "id": "260322009",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/22/f232349a197c4b239ae4cbdb9df232e5-20260322110718-0s.webp?a=1",
            "description": "Motor bukan cuma soal jalan, tapi juga soal gaya! Aksesori yang tepat bisa bikin motor kamu makin ganteng sekaligus lebih nyaman dipakai harian. Mulai dari tampilan sampai fungsi, semuanya bisa di-upgrade sesuai selera. Tapi ingat, modifikasi tetap harus sesuai aturan ya, biar keren tanpa masalah di jalan. Mana aksesori favorit kamu?",
            "duration": 86,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/22/f232349a197c4b239ae4cbdb9df232e5-20260322110647-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/22 11:09:00",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/22/f232349a197c4b239ae4cbdb9df232e5.smil/playlist.m3u8",
            "tag": "motor,aksesoris motor",
            "title": "Video 3 Aksesoris Motor Yang Bikin Keren dan Lebih Nyaman",
            "unixtime": 1774152540000,
            "videourl": "https://20.detik.com/detikupdate/20260322-260322009/video-3-aksesoris-motor-yang-bikin-keren-dan-lebih-nyaman"
        },
        {
            "id": "260323132",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/bc2cf8eeafe54a1789aac2d9e58a2994-20260323163838-0s.webp?a=1",
            "description": "Rekayasa lalu lintas sistem one way diberlakukan dari kawasan Puncak, Bogor, menuju Jakarta pada H+2 Lebaran 2026. Hingga sore hari, lebih dari 21 ribu kendaraan tercatat melintas, dengan arus lalu lintas terpantau lancar.",
            "duration": 31,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/23/bc2cf8eeafe54a1789aac2d9e58a2994-20260323163852-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/23 16:46:22",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/23/bc2cf8eeafe54a1789aac2d9e58a2994.smil/playlist.m3u8",
            "tag": "one way simpang gadog puncak,simpang gadok,arus balik,bogor",
            "title": "Video: One Way Diberlakukan, 21 Ribu Kendaraan Melintas dari Puncak ke Jakarta",
            "unixtime": 1774259182000,
            "videourl": "https://20.detik.com/detikupdate/20260323-260323132/video-one-way-diberlakukan-21-ribu-kendaraan-melintas-dari-puncak-ke-jakarta"
        },
        {
            "id": "260319038",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2026/03/19/2daa6d8f0cbc46aba1e754c3e5e73f91-20260319202912-0s.webp?a=1",
            "description": "Viral di media sosial menunjukkan rombongan pikap impor asal India yang turut terjebak kemacetan bersama para pemudik di Tol Cipali. Kendaraan yang telah ditempeli stiker 'Kopdes Merah Putih' itu diduga sedang dalam proses pengiriman ke lokasi tujuan.",
            "duration": 73,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://akcdn.detik.net.id/community/media/visual/2026/03/19/pick-mahindra-1773927590456_916.jpeg?w=620",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2026/03/19 20:39:14",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2026/03/19/2daa6d8f0cbc46aba1e754c3e5e73f91.smil/playlist.m3u8",
            "tag": "kopdes merak putih,pick up mahindra",
            "title": "Video Rombongan Pick Up India Ikut Macet-macetan Sama Pemudik di Tol Cipali",
            "unixtime": 1773927554000,
            "videourl": "https://20.detik.com/detikupdate/20260319-260319038/video-rombongan-pick-up-india-ikut-macetmacetan-sama-pemudik-di-tol-cipali"
        },
        {
            "id": "241225088",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2024/12/25/1535434f8e974f41a95e41fd6bc579ac-20241225190241-0s.webp?a=1",
            "description": "Bagi yang mau menikah atau belum punya pasangan di sini ada info menarik! Khususnya kamu warga Yogyakarta, kamu bisa ikut acara ini secara gratis. Dilansir dari detikJogja, berikut informasi selengkapnya...",
            "duration": 130,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2024/12/25/Rev_Yang_Mau_Nikah_Gratis_atau_Car_saXPtnL-20241225190412-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2024/12/25 18:42:19",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2024/12/25/1535434f8e974f41a95e41fd6bc579ac.smil/playlist.m3u8",
            "tag": "nikah gratis,nikah gratis jogja,cari jodoh",
            "title": "Video: Yang Mau Nikah Gratis atau Cari Jodoh 2025 Merapat, Simak Caranya Ya!",
            "unixtime": 1735126939000,
            "videourl": "https://20.detik.com/detikupdate/20241225-241225088/video-yang-mau-nikah-gratis-atau-cari-jodoh-2025-merapat-simak-caranya-ya"
        },
        {
            "id": "250416090",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/16/d41e015880c9499f8e9896c7d54a9d52-20250416151248-0s.webp?a=1",
            "description": "Gedung tertinggi di dunia yang baru bakal lahir di Riyadh! Dengan tinggi 2.000 meter dan 678 lantai, bangunan ini akan berdiri di kawasan CBD North Pole. Dirancang oleh Foster \u0026 Partners, dan digarap bareng perusahaan global seperti Aecom \u0026 Bechtel. Proyek ini bisa bikin Arab Saudi jadi pusat bisnis \u0026 arsitektur modern dunia!",
            "duration": 89,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/16/Burj_Khalifa_Lewat_Arab_Bakal_Bang_kBYxpgo-20250416151455-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/16 15:12:46",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/16/d41e015880c9499f8e9896c7d54a9d52.smil/playlist.m3u8",
            "tag": "arab,gedung tertinggi,burj khalifa",
            "title": "Video: Burj Khalifa Lewat! Arab Bakal Bangun Gedung Super Tinggi 2.000 Meter",
            "unixtime": 1744791166000,
            "videourl": "https://20.detik.com/detikupdate/20250416-250416090/video-burj-khalifa-lewat-arab-bakal-bangun-gedung-super-tinggi-2000-meter"
        },
        {
            "id": "250301053",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/03/01/aaa1ba4dc3e847648a8f0c2e717d16e2-20250301081349-0s.webp?a=1",
            "description": "Warga Kecamatan Amfoang Utara, Kabupaten Kupang, membawa jenazah bayi perempuan asal Desa Fatunaus dengan sepeda motor. Hal ini dilakukan karena jalan setempat rusak parah dan tidak bisa dilalui kendaraan roda empat.",
            "duration": 54,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/03/01/aaa1ba4dc3e847648a8f0c2e717d16e2-20250301081420-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/03/01 08:14:09",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/03/01/aaa1ba4dc3e847648a8f0c2e717d16e2.smil/playlist.m3u8",
            "tag": "kupang,amfoang utara,jalan rusak",
            "title": "Video: Warga Kupang Bawa Peti Jenazah Bayi Pakai Motor Karena Jalan Rusak Parah",
            "unixtime": 1740791649000,
            "videourl": "https://20.detik.com/detikupdate/20250301-250301053/video-warga-kupang-bawa-peti-jenazah-bayi-pakai-motor-karena-jalan-rusak-parah"
        },
        {
            "id": "241225091",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2024/12/25/ccabf876456d43fab65c290b6ab9695a-20241225191407-0s.webp?a=1",
            "description": "Wisatawan asal Jakarta Selatan (Jaksel) Muhammad Farih Ibrahim (18), bercerita pernah digetok Rp 700 ribu oleh joki jalur alternatif di Puncak, Bogor, Jawa Barat. Ia pun enggan menggunakan joki jalur alternatif saat berwisata ke Puncak selanjutnya.",
            "duration": 115,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2024/12/25/ccabf876456d43fab65c290b6ab9695a-20241225191326-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2024/12/25 19:12:42",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2024/12/25/ccabf876456d43fab65c290b6ab9695a.smil/playlist.m3u8",
            "tag": "bogor,jalur alternatif",
            "title": "Video Wisatawan Kapok Digetok Jalur Alternatif Rp 700 Ribu di Puncak",
            "unixtime": 1735128762000,
            "videourl": "https://20.detik.com/detikupdate/20241225-241225091/video-wisatawan-kapok-digetok-jalur-alternatif-rp-700-ribu-di-puncak"
        },
        {
            "id": "250228081",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/02/28/bfc23043bf1346d698b81877ccf6e447-20250228130814-0s.webp?a=1",
            "description": "Muncul lubang runtuhan atau sinkhole di ruas jalan utama Sendang, Tulungagung, Jawa Timur. Sinkhole ini diduga muncul akibat rembesan air dari selokan.",
            "duration": 63,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/02/28/bfc23043bf1346d698b81877ccf6e447-20250228130911-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/02/28 13:08:23",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/02/28/bfc23043bf1346d698b81877ccf6e447.smil/playlist.m3u8",
            "tag": "sinkhole,jalan amblas,tulungagung",
            "title": "Video: Sinkhole Sedalam 8 Meter Muncul di Jalan Tulungagung",
            "unixtime": 1740722903000,
            "videourl": "https://20.detik.com/detikupdate/20250228-250228081/video-sinkhole-sedalam-8-meter-muncul-di-jalan-tulungagung"
        },
        {
            "id": "240925055",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2024/09/25/88a158058232463d9cc591c69f813dff-20240925080453-0s.webp?a=1",
            "description": "M2M tiba-tiba muncul di media sosial dengan membawakan lagu 'The Day You Went Away' versi akustik. Penampilan mereka tentu mengejutkan penggemar",
            "duration": 67,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2024/09/25/Video-_M2M_Posting_The_Day_You_Wen_H4NYIzV-20240925080647-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2024/09/25 07:59:30",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2024/09/25/88a158058232463d9cc591c69f813dff.smil/playlist.m3u8",
            "tag": "m2m,the day you went away",
            "title": "Video: M2M Posting 'The Day You Went Away' Versi Akustik, Bakal Reuni?",
            "unixtime": 1727225970000,
            "videourl": "https://20.detik.com/detikupdate/20240925-240925055/video-m2m-posting-the-day-you-went-away-versi-akustik-bakal-reuni"
        },
        {
            "id": "250218124",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/02/18/180ccbdd0f794f8ca04645e1fd05d9a1-20250218205259-0s.webp?a=1",
            "description": "Aktor Taiwan Darren Wang dan sembilan orang lainnya ditangkap pada Selasa (18/2) pagi atas dugaan penghindaran wajib militer dan pemalsuan dokumen. Mereka telah ditahan oleh petugas biro investigasi kriminal setempat.",
            "duration": 31,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/02/18/Aktor_Taiwan_Darren_Wang_Ditangkap_sbdibFl-20250218205401-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/02/18 21:00:42",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/02/18/180ccbdd0f794f8ca04645e1fd05d9a1.smil/playlist.m3u8",
            "tag": "darren wang,darren wang ditangkap polisi",
            "title": "Video: Aktor Taiwan Darren Wang Ditangkap Polisi, Kenapa?",
            "unixtime": 1739887242000,
            "videourl": "https://20.detik.com/detikupdate/20250218-250218124/video-aktor-taiwan-darren-wang-ditangkap-polisi-kenapa"
        },
        {
            "id": "250421155",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/21/989ebd5df7374572954899fee0f847b6-20250421224410-0s.webp?a=1",
            "description": "Patung biawak di Desa Krasak Kecamatan Selomerto, Wonosobo, viral di media sosial. Patung setinggi 7 meter ramai diperbincangkan gegara mirip dengan biawak asli.",
            "duration": 93,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/21/Video_Melihat_Patung_Biawak_di_Won_MH5fWxK-20250421224502-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/21 22:42:57",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/21/989ebd5df7374572954899fee0f847b6.smil/playlist.m3u8",
            "tag": "patung,biawak,seni,viral,wonosobo,birojatengdiy",
            "title": "Video: Melihat Patung Biawak di Wonosobo yang Viral gegara Mirip Asli",
            "unixtime": 1745250177000,
            "videourl": "https://20.detik.com/detikupdate/20250421-250421155/video-melihat-patung-biawak-di-wonosobo-yang-viral-gegara-mirip-asli"
        },
        {
            "id": "250524092",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/05/24/9ce647d2336d43ee8f13b58e28c0925a-20250524195704-0s.webp?a=1",
            "description": "Pemerintah akan memberikan bantuan subsidi upah (BSU) kepada pekerja. Lantas, apa syaratnya?",
            "duration": 47,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/05/24/9ce647d2336d43ee8f13b58e28c0925a-20250524195628-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/05/24 18:53:45",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/05/24/9ce647d2336d43ee8f13b58e28c0925a.smil/playlist.m3u8",
            "tag": "bantuan subsidi upah,bsu,pekerja",
            "title": "Video: Hore! Akan Ada Bantuan Subsidi Upah Bagi Pekerja, Ini Syaratnya",
            "unixtime": 1748087625000,
            "videourl": "https://20.detik.com/detikupdate/20250524-250524092/video-hore-akan-ada-bantuan-subsidi-upah-bagi-pekerja-ini-syaratnya"
        },
        {
            "id": "250604161",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/06/04/a1822153a9be49ff832b261279eec01d-20250604182747-0s.webp?a=1",
            "description": "Kejaksaan Negeri (Kejari) Sukabumi melakukan penggeledahan di Kantor Dinas Lingkungan Hidup (DLH) Kabupaten Sukabumi. Dalam penggeledahan itu, petugas menyita puluhan dokumen serta satu unit laptop. Penggeledahan ini berkaitan dengan kasus dugaan korupsi pengelolaan sampah. detikers tonton video menarik lainnya disini...",
            "duration": 61,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/06/04/a1822153a9be49ff832b261279eec01d-20250604182641-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/06/04 19:12:17",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/06/04/a1822153a9be49ff832b261279eec01d.smil/playlist.m3u8",
            "tag": "penggeledahan,sukabumi 1980,dinas lingkungan hidup,kabupaten sukabumi,sukabumi",
            "title": "Video Kejari Geledah Kantor DLH Sukabumi, Sita 50 Dokumen-Laptop",
            "unixtime": 1749039137000,
            "videourl": "https://20.detik.com/detikupdate/20250604-250604161/video-kejari-geledah-kantor-dlh-sukabumi-sita-50-dokumenlaptop"
        },
        {
            "id": "241124093",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2024/11/24/b107dad5ab7749e0a09900f61d7f4755-20241124213440-0s.webp?a=1",
            "description": "The Adams tampil di Plainsong Live Stage Joyland Jakarta 2024 pukul 17.05 WIB. Meski hujan turun, penonton tetap antusias memeriahkan suasana di Gelora Bung Karno.",
            "duration": 37,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2024/11/24/b107dad5ab7749e0a09900f61d7f4755-20241124213335-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2024/11/24 21:35:00",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2024/11/24/b107dad5ab7749e0a09900f61d7f4755.smil/playlist.m3u8",
            "tag": "the adams,joyland jakarta 2024,joyland",
            "title": "Video: Hujan-hujanan Bareng The Adams di Joyland Jakarta 2024",
            "unixtime": 1732458900000,
            "videourl": "https://20.detik.com/detikupdate/20241124-241124093/video-hujanhujanan-bareng-the-adams-di-joyland-jakarta-2024"
        },
        {
            "id": "250408075",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/08/e074b5ed92e544759d8ecba3f3bfd38d-20250408113505-0s.webp?a=1",
            "description": "Libur panjang memang memberikan banyak waktu untuk bersenang-senang, mulai dari bersantai, menghabiskan waktu bersama keluarga, hingga bepergian ke berbagai tempat wisata. Namun, setelah momen-momen menyenangkan itu berakhir, tak jarang muncul perasaan sedih, malas, dan bahkan cemas saat harus kembali ke rutinitas harian. Fenomena ini dikenal juga dengan istilah 'Post-Holiday Blues'.",
            "duration": 76,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/08/IMG_7672-20250408113617-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/08 11:34:30",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/08/e074b5ed92e544759d8ecba3f3bfd38d.smil/playlist.m3u8",
            "tag": "post-holiday blues",
            "title": "Video: Habis Libur Panjang Malah Sedih dan Cemas, Kenapa Ya?",
            "unixtime": 1744086870000,
            "videourl": "https://20.detik.com/detikupdate/20250408-250408075/video-habis-libur-panjang-malah-sedih-dan-cemas-kenapa-ya"
        },
        {
            "id": "250418054",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/18/8eba01373c12431099aa5f4e18626744-20250418095958-0s.webp?a=1",
            "description": "Seorang bocah berusia 3 tahun di Jember, Jawa Timur, mengeluh sulit buang air besar (BAB) yang membuat perutnya membesar. Setelah diperiksa, ternyata ada cacing bersarang di ususnya. Kasus ini pertama kali dimuat di jurnal medis Journal of Medical Case Report. Bocah itu dilarikan ke RSD dr Soebandi, Jember dengan keluhan konstipasi dan perut kembung selama 3 hari.",
            "duration": 42,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/18/Cacing_yang_ditemukan_selama_opera_CQ1sxwb-20250418100056-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/18 09:55:31",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/18/8eba01373c12431099aa5f4e18626744.smil/playlist.m3u8",
            "tag": "cacing,usus,anak,kesehatan,kesehatan anak",
            "title": "Video: Penampakan Cacing di Usus Bocah 3 Tahun di Jember",
            "unixtime": 1744944931000,
            "videourl": "https://20.detik.com/detikupdate/20250418-250418054/video-penampakan-cacing-di-usus-bocah-3-tahun-di-jember"
        },
        {
            "id": "250421082",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/21/34cff054006645bab6618b9fd1aa7241-20250421132325-0s.webp?a=1",
            "description": "Tarif MRT Rp 1 berlaku khusus perempuan pada Hari Kartini (21/4). Momen ini dimanfaatkan oleh perempuan-perempuan di Jakarta untuk berkeliling, seperti Indri (62) dan teman-temannya.",
            "duration": 81,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/21/Ibu-ibu_Berkebaya_Keliling_Jakarta_IE09LMQ-20250421132710-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/21 13:23:19",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/21/34cff054006645bab6618b9fd1aa7241.smil/playlist.m3u8",
            "tag": "mrt,hari kartini",
            "title": "Video: Ibu-ibu Berkebaya Keliling Jakarta, Manfaatkan Tarif MRT Rp 1",
            "unixtime": 1745216599000,
            "videourl": "https://20.detik.com/detikupdate/20250421-250421082/video-ibuibu-berkebaya-keliling-jakarta-manfaatkan-tarif-mrt-rp-1"
        },
        {
            "id": "250415087",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/15/ec02182fe9fb4a4995becfb2b88e6a9d-20250415141048-0s.webp?a=1",
            "description": "Band rock asal AS, Green Day, menjadi perbincangan saat manggung di festival Coachella. Billie Joe cs suarakan dukungannya ke Palestina dengan mengubah lirik lagu saat bawakan 'American Idiot'.",
            "duration": 54,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/04/15/Green_Day_Ubah_Lirik_Lagu_Dukung_P_KO5v14D-20250415141301-custom.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2025/04/15 14:30:43",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/04/15/ec02182fe9fb4a4995becfb2b88e6a9d.smil/playlist.m3u8",
            "tag": "green day,green day coachella,coachella,green day american idiot,green day palestina,palestina",
            "title": "Video: Green Day Ubah Lirik Lagu Dukung Palestina Saat Tampil di Coachella",
            "unixtime": 1744702243000,
            "videourl": "https://20.detik.com/detikupdate/20250415-250415087/video-green-day-ubah-lirik-lagu-dukung-palestina-saat-tampil-di-coachella"
        },
        {
            "id": "240925135",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2024/09/25/58d16e23c1464555b0313a906d4f06db-20240925205508-0s.webp?a=1",
            "description": "Pembalap Elf Marc VDS Racing, Filip Salac melakukan aksi kocak di salah satu pantai di Kuta Mandalika, Lombok Tengah, Nusa Tenggara Barat (NTB). Ia mendadak menjadi penjual es krim di tengah-tengah liburannya menjelang balapan di Sirkuit Mandalika pada 27-29 September 2024.",
            "duration": 38,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2024/09/25/58d16e23c1464555b0313a906d4f06db-20240925205434-0s.jpg",
            "is_vertical_video": "1",
            "programid": "221213591",
            "programname": "detikUpdate",
            "publishdate": "2024/09/25 20:40:35",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2024/09/25/58d16e23c1464555b0313a906d4f06db.smil/playlist.m3u8",
            "tag": "filip salac,moto2,pembalap moto2,motogp mandalika",
            "title": "Video Aksi Kocak Pembalap Moto2 Dagang Es Krim di Pantai Mandalika",
            "unixtime": 1727271635000,
            "videourl": "https://20.detik.com/detikupdate/20240925-240925135/video-aksi-kocak-pembalap-moto2-dagang-es-krim-di-pantai-mandalika"
        },
        {
            "id": "251202059",
            "animated": "https://cdnv.detik.com/videoservice/AdminTV/2025/12/02/32ef7ae61d264cf9b128fd4c101e6199-20251202163523-0s.webp?a=1",
            "description": "Sobat Sabtu Goes to Ragunan!",
            "duration": 58,
            "type": "ChannelsKeywordsNoCache",
            "imageurl": "https://cdnv.detik.com/videoservice/AdminTV/2025/12/02/32ef7ae61d264cf9b128fd4c101e6199-20251202163522-0s.jpg",
            "is_vertical_video": "1",
            "programid": "250729609",
            "programname": "Community Connect",
            "publishdate": "2025/12/02 16:08:50",
            "smil": "https://vod.detik.com/mc/_definst_/smil:http/mc/video/detiktv/videoservice/AdminTV/2025/12/02/32ef7ae61d264cf9b128fd4c101e6199.smil/playlist.m3u8",
            "tag": "community connect,komunitas sobat sabtu",
            "title": "Sobat Sabtu Goes to Ragunan!",
            "unixtime": 1764666530000,
            "videourl": "https://20.detik.com/community-connect/20251202-251202059/sobat-sabtu-goes-to-ragunan"
        }
    ],
    "debug": {
        "profile": {
            "cluster": 6,
            "keywordStats": [],
            "channelStats": [],
            "categoryStats": [],
            "readDocs": [
                "-"
            ],
            "recommendedDocs": null,
            "lastProfileAccess": 0
        },
        "mostpopCluster": null,
        "topPageDocs": null
    }
}




curl 'https://applets.ebxcdn.com/applets/www.detik.com/scripts.js' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://www.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://www.detik.com/api/jadwalsholat/kota-jakarta' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmb=146380193.1.10.1774261778; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261921$j60$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g0$t1774261921$j60$l0$h0' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://www.google.com/ccm/collect?frm=0&ae=g&en=page_view&dl=https%3A%2F%2Fwww.detik.com%2F&scrsrc=www.googletagmanager.com&rnd=709169925.1774261922&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&auid=997881967.1774261778&navt=r&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115616986~115938466~115938469~116024733~117484252~118131589&apve=1&apvf=f&apvc=1&tft=1774261922007&tfd=5935' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://www.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261921756&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=0&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115616986~115938466~115938469~116024733~117484252~118104772&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fwww.detik.com%2F&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&en=page_view&tfd=6185' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://20.detik.com/api/statuslive/wpnewsfeed_2' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://recg.detik.com/article-recommendation/wp/146380193.1399813887.1774261778?size=9&nocache=1&ids=undefined&acctype=acc-detikcom' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261922$j59$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g1$t1774261922$j59$l0$h0; __dtmb=146380193.2.10.1774261922' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://recg.detik.com/article-recommendation/sticky/146380193.1399813887.1774261778?size=6&nocache=1&ids=undefined&acctype=acc-detikcom' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261922$j59$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g1$t1774261922$j59$l0$h0; __dtmb=146380193.2.10.1774261922' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fdetail-polling%2F&scrsrc=www.googletagmanager.com&rnd=582882880.1774261923&dt=Polling&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115616985~115938465~115938468~116024733~117266400~117484252&apve=1&apvf=f&apvc=1&tft=1774261922925&tfd=682' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://20.detik.com/api/statuslive/livestreaming' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://www.detik.com/ajax/newsfeed_recommendation_wp' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261922$j59$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g1$t1774261922$j59$l0$h0; __dtmb=146380193.2.10.1774261922' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' ;
curl 'https://sp-trk.com/i/jb7wac2q?lc=https%3A%2F%2Fwww.detik.com%2F&hl=2&tp=0&if=0&te=0&so=landscape-primary&bp=Linux%20x86_64&lg=en-US&sw=1920&sh=1200&sl=0&st=0&sx=0&sy=0&ow=1878&oh=1092&aw=1920&ah=1200&cd=24&pr=1&tz=Asia%2FJakarta&to=-420&pc=12&dm=8&ss=1&ls=1&tu=4230289565901460152&u=4230289562730566278&iu=4230289565901460152&il=https%3A%2F%2Fwww.detik.com%2F&su=4230289565901460152&np=def&id=1&od=0&pe=1&gp=Google%20Inc.%20(Intel)%7CANGLE%20(Intel%2C%20Mesa%20Intel(R)%20Graphics%20(ADL%20GT2)%2C%20OpenGL%20ES%203.2)&co=0&jv=0&ww=756&wh=1011&ne=4g&nr=250&nd=3.45&es=33&hq=1&cw=1&pb1=-1267231041&pb2=-1267231041&pn=-1646160397&pt=39&pd=0&t=01&a=1774261922954&r=4230292044382798101&o=4xxxmm4lv2m&et=57&n=pv' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Content-type: text/plain; charset=utf-8' \
  -H 'Origin: https://www.detik.com' \
  -H 'Referer: https://www.detik.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=1810704395.1774261923&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115938465~115938468~116024733~117384406~117484252&apve=1&apvf=f&apvc=1&tft=1774261923126&tfd=841' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://www.detik.com/ajax/newsfeed_recommendation_sticky' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261922$j59$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g1$t1774261922$j59$l0$h0; __dtmb=146380193.2.10.1774261922' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' ;
curl 'https://collent.detik.com/list' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '[{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8412182","spm":"desktop$##$detikcom$##$gianthltemanmudik$##$1"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true}]' ;
curl 'https://newpolong.detik.com/api/graphqlv2/' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json' \
  -b 'dtklucx=gen_2b7799d8-ce08-8968-080d-492839146268; _gcl_au=1.1.997881967.1774261778; __dtma=146380193.1399813887.1774261778.1774261778.1774261778.1; __dtmc=146380193; _ga=GA1.1.49311229.1774261780; _pk_id.20.33e9=59cf8287710dbd30.1774261781.; _pk_ses.20.33e9=1; csrftoken=SiRyNuoLA5iCKEmSPN1FXNCC09frLAT4V4VucxRMEMdzzP64ewGDk5I00hjJAh8y; _ga_Y7WW684XXD=GS2.1.s1774261779$o1$g1$t1774261922$j59$l0$h0; _ga_CY42M5S751=GS2.1.s1774261780$o1$g1$t1774261922$j59$l0$h0; __dtmb=146380193.2.10.1774261922' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/frontend_polong/detail-polling/?pollId=null&isEmbed=false' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '{"query":"\n        query {\n          pollingDetail(programId:\"null\") \n          {       \n            id\n            title\n            text\n            imageUrl\n            number\n            createdDate\n            startDate\n            endDate\n            remainingDays\n            remainingHours\n            options {\n                id\n                text\n                imageUrl\n            }\n            channel{\n              id\n              color\n              name\n              image\n            }\n            articleUrl\n            mode\n            participants\n            comments\n          }\n        }\n        "}' ;
curl 'https://20.detik.com/api/statuslive/livestreaming_sponsorship' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=1972853073.1774261923&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115938466~115938468~116024733~117484252&apve=1&apvf=f&apvc=1&tft=1774261923272&tfd=846' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=178211286.1774261923&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115938465~115938469~116024733~117484252~118104773&apve=1&apvf=f&apvc=1&tft=1774261923386&tfd=850' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261922578&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938465~115938469~116024733~117484252~118131588&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fdetail-polling%2F%3FpollId%3Dnull%26isEmbed%3Dfalse&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Polling&en=page_view&tfd=1219' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=615931973.1774261924&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115938466~115938468~116024733~117484252&apve=1&apvf=f&apvc=1&tft=1774261923546&tfd=941' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261922635&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938465~115938468~116024733~117484252~118104771&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjQ%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1294' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=1560446145.1774261924&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115938465~115938468~116024733~117484252&apve=1&apvf=f&apvc=1&tft=1774261923663&tfd=967' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261922739&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938466~115938469~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjM%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1328' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://www.google.com/ccm/collect?frm=2&ae=g&en=page_view&dr=www.detik.com&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F&scrsrc=www.googletagmanager.com&rnd=1847225224.1774261924&dt=Cb%20Polling%20Single&auid=997881967.1774261778&navt=n&npa=0&ep.ads_data_redaction=0&gtm=45He63i0v72264312za200zd72264312xea&gcd=13l3l3l3l1l1&dma=0&tag_exp=103116026~103200004~115616986~115938465~115938469~116024733~117484252&apve=1&apvf=f&apvc=1&tft=1774261923821&tfd=1003' \
  -X 'POST' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'Referer: https://newpolong.detik.com/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261922856&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115616986~115938465~115938468~116024733~117484252~118128922&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjI%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1333' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261923049&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938466~115938469~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjE%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1279' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261923175&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115616985~115938465~115938469~116024733~117484252~118104771&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjA%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1278' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259z872264312za20gzb72264312zd72264312&_p=1774261923333&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938465~115938468~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NTg%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=page_view&tfd=1223' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261921756&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=0&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115616986~115938466~115938469~116024733~117484252~118104772&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fwww.detik.com%2F&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&en=scroll&epn.percent_scrolled=90&tfd=11186' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-CY42M5S751&gtm=45je63i0v873223606z872264312za20gzb72264312zd72264312&_p=1774261921756&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=0&pscdl=noapi&_eu=AAAAAGQ&_s=1&tag_exp=103116026~103200004~115938466~115938469~116024733~117484252~117884344~118131588&sid=1774261780&sct=1&seg=1&dl=https%3A%2F%2Fwww.detik.com%2F&dt=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&en=page_view&ep.kanalId=2&ep.keyword=berita%20hari%20ini%2C%20berita%20terkini%2C%20berita%20terbaru%2C%20info%20berita%2C%20peristiwa%2C%20kecelakaan%2C%20kriminal%2C%20hukum%2C%20berita%20unik%2C%20Politik%2C%20liputan%20khusus%2C%20Indonesia%2C%20Internasional&ep.contentType=wp&ep.platform=desktop&ep.originalTitle=detikcom%20-%20Informasi%20Berita%20Terkini%20dan%20Terbaru%20Hari%20Ini&ep.namaKanal=detikcom&ep.pwa_traffic=false&up.pwa_traffic_user=false&tfd=11282' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261922578&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115938465~115938469~116024733~117484252~118131588&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fdetail-polling%2F%3FpollId%3Dnull%26isEmbed%3Dfalse&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Polling&en=scroll&epn.percent_scrolled=90&tfd=6532' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261922635&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115938465~115938468~116024733~117484252~118104771&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjQ%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=6491' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261922739&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115938466~115938469~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjM%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=6351' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261922856&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115616986~115938465~115938468~116024733~117484252~118128922&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjI%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=7239' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261923049&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115938466~115938469~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjE%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=7170' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261923175&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115616985~115938465~115938469~116024733~117484252~118104771&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NjA%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=7080' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://analytics.google.com/g/collect?v=2&tid=G-Y7WW684XXD&gtm=45je63i0v897491259za20gzb72264312zd72264312&_p=1774261923333&gcd=13l3l3l3l1l1&npa=0&dma=0&cid=49311229.1774261780&ul=en-us&sr=1920x1200&uaa=x86&uab=64&uafvl=Not-A.Brand%3B24.0.0.0%7CChromium%3B146.0.7818.31&uamb=0&uam=&uap=Linux&uapv=&uaw=0&are=1&frm=2&pscdl=noapi&_eu=AEAAAGQ&_s=2&tag_exp=103116026~103200004~115938465~115938468~116024733~117484252&sid=1774261779&sct=1&seg=1&dl=https%3A%2F%2Fnewpolong.detik.com%2Ffrontend_polong%2Fslider-polling%2F%3FpollId%3DUHJvZ3JhbXNOb2RlOjE2NTg%3D&dr=https%3A%2F%2Fwww.detik.com%2F&dt=Cb%20Polling%20Single&en=scroll&epn.percent_scrolled=90&tfd=6959' \
  -X 'POST' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-length: 0' \
  -H 'origin: https://newpolong.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://newpolong.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-storage-access: none' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  -H 'x-client-data: CIuNywE=' ;
curl 'https://rech20.detik.com/article-recommendation/wp/146380193.1399813887.1774261778' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '{"size":25,"excludeProgramIds":["170724519","190313542"],"excludeDocs":["260323011","260323008","260322008","260323005","260322016"],"isVertical":true}' ;
curl 'https://collent.detik.com/list' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '[{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8412503","spm":"desktop$##$detikcom$##$boxpilihanredaksi$##$1"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8412448","spm":"desktop$##$detikcom$##$boxpilihanredaksi$##$2"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8412447","spm":"desktop$##$detikcom$##$boxpilihanredaksi$##$3"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8412453","spm":"desktop$##$detikcom$##$boxpilihanredaksi$##$4"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"8411708","spm":"desktop$##$detikcom$##$boxpilihanredaksi$##$5"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true}]' ;
curl 'https://collent.detik.com/list' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'origin: https://www.detik.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.detik.com/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '[{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260323011","spm":"desktop$##$detikcom$##$boxflash$##$1"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260323008","spm":"desktop$##$detikcom$##$boxflash$##$2"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260322008","spm":"desktop$##$detikcom$##$boxflash$##$3"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260323005","spm":"desktop$##$detikcom$##$boxflash$##$4"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260322016","spm":"desktop$##$detikcom$##$boxflash$##$5"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true},{"eventName":"show","eventData":{"enter_from_doc_id":"","doc_id":"260323129","spm":"desktop$##$detikcom$##$boxflash$##$6"},"dtma":"146380193.1399813887.1774261778.1774261778.1774261778.1","dtkluc":"gen_2b7799d8-ce08-8968-080d-492839146268","visibility":true}]'
