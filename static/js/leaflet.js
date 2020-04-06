let position;

$(function(){
        function createMap(){
                //地図を表示するdiv要素のidを設定
                let map = L.map('mapcontainer');
                //地図の中心とズームレベルを指定
                map.setView([34.60, 135.47], 11);
                //表示するタイルレイヤのURLとAttributionコントロールの記述を設定して、地図に追加する
                L.tileLayer(
                        'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
                        {
                        attribution: "<a href='https://maps.gsi.go.jp/development/ichiran.html' target='_blank'>地理院タイル</a>"
                        }
                ).addTo(map);
                let p = position;
                console.log(p);
                let latlng, name, loc;
                for(var i=0;i<p[0].length;++i){
                        name = p[0][i];
                        loc = p[1][i];
latlng = [p[2][i], p[3][i]];
L.marker(latlng).addTo(map)
        .bindPopup("<b>"+name+"</b><br>"+loc)
        .openPopup();
}
//スケールコントロールを最大幅200px、右下、m単位で地図に追加
L.control.scale({ maxWidth: 200, position: 'bottomright', imperial: false }).addTo(map);
//ズームコントロールを左下で地図に追加
L.control.zoom({ position: 'bottomleft' }).addTo(map);
}
//CSVファイルを読み込む関数getCSV()の定義
function getCSV(){
var req = new XMLHttpRequest(); // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
req.overrideMimeType("text/plain; charset=shift_jis");
req.open("get", "/static/exvs2_pref27.csv", true); // アクセスするファイルを指定
req.send(null); // HTTPリクエストの発行
// レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ
req.onload = function(){
let result = convertCSVtoArray(req.responseText); // 渡されるのは読み>込んだCSVデータ
position = result;
console.log(result);
createMap();
}
}
function convertCSVtoArray(str){ // 読み込んだCSVデータが文字列として渡される
var result = []; // 最終的な二次元配列を入れるための配列
var tmp = str.split("\n"); // 改行を区切り文字として行を要素とした配列を生成

// 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
for(var i=0;i<tmp.length;++i){
if(tmp[i]==""){
tmp.splice(i,1);
break;
}
result[i] = tmp[i].split(',');
}
return result;
}
getCSV();
$("input").on("change", function(){
let lat = $("#maplat").val();
let lng = $("#maplng").val();
let level = $("#maplevel").val();
var map = L.map('mapcontainer');
map.setView([lat, lng], level);
console.log();
});
});