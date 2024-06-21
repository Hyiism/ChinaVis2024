<template>
  <div ref="bubbleChartContainer" class="bubble-chart-container">
    <div ref="bubbleChart"></div>
  </div>
</template>

<script>
import * as d3v5 from 'd3v5';

export default {
  data() {
    return {
      rawdata: [
        {
          "timeFrame": "Africa",
          "color": "Climate change",
          "freq": 64.7,
          "index": 0,
          "x": 39.445354829121925,
          "y": 194.81755109337433,
          "vy": 0.000020138042427761092,
          "vx": 0.0003180788166611488
        },
        {
          "timeFrame": "Africa",
          "color": "Global warming",
          "freq": 45,
          "index": 1,
          "x": 36.69751660394721,
          "y": 231.16875240073193,
          "vy": -0.000008125286625464061,
          "vx": 0.00021357770291715258
        },
        {
          "timeFrame": "Africa",
          "color": "Greenhouse gas",
          "freq": 40.5,
          "index": 2,
          "x": 62.36664699328221,
          "y": 167.44152139789176,
          "vy": -0.00009946544327330508,
          "vx": -0.00011852131801429358
        },
        {
          "timeFrame": "Africa",
          "color": "Deforestation",
          "freq": 30,
          "index": 3,
          "x": 73.20118796600451,
          "y": 195.47092794391747,
          "vy": -0.00012097683366135063,
          "vx": -0.00005828704473717648
        },
        {
          "timeFrame": "Africa",
          "color": "Carbon dioxide",
          "freq": 29.6,
          "index": 4,
          "x": 32.93213641341683,
          "y": 161.78833345851305,
          "vy": 0.00010232989535857217,
          "vx": -0.00009873934400481765
        },
        {
          "timeFrame": "Africa",
          "color": "Air pollution",
          "freq": 27.7,
          "index": 5,
          "x": 65.3746232264108,
          "y": 241.11674615057322,
          "vy": 0.00017015203423018728,
          "vx": -0.000261112569096808
        },
        {
          "timeFrame": "Africa",
          "color": "Biodiversity",
          "freq": 27.5,
          "index": 6,
          "x": 45.93623970577083,
          "y": 260.0219898765374,
          "vy": 0.00012565909195423275,
          "vx": -0.0003047538349851563
        },
        {
          "timeFrame": "Africa",
          "color": "Donald Trump",
          "freq": 27.2,
          "index": 7,
          "x": 50.308165899508865,
          "y": 140.5465996826362,
          "vy": -0.000031796872106161794,
          "vx": -0.00027232124249394274
        },
        {
          "timeFrame": "Africa",
          "color": "Coronavirus",
          "freq": 16.6,
          "index": 8,
          "x": 60.55552132878105,
          "y": 217.0522850244582,
          "vy": 0.00006579574179426557,
          "vx": 0.000259354724103948
        },
        {
          "timeFrame": "Sud America",
          "color": "Climate change",
          "freq": 38.8,
          "index": 9,
          "x": 180.45986610763407,
          "y": 241.59651921385895,
          "vy": 0.00006611057301751824,
          "vx": 0.00010941705356985378
        },
        {
          "timeFrame": "Sud America",
          "color": "Global warming",
          "freq": 33.2,
          "index": 10,
          "x": 179.86083260228725,
          "y": 162.7844995033854,
          "vy": 0.000035512553822727995,
          "vx": 0.0002073639834474341
        },
        {
          "timeFrame": "Sud America",
          "color": "Deforestation",
          "freq": 33.2,
          "index": 11,
          "x": 207.31113832817238,
          "y": 227.37095295042124,
          "vy": 0.00000651861653412188,
          "vx": -0.00010165866170747482
        },
        {
          "timeFrame": "Sud America",
          "color": "Amazon rainforest",
          "freq": 32.3,
          "index": 12,
          "x": 205.9463566947302,
          "y": 149.6764802916291,
          "vy": -0.00008137541785537544,
          "vx": -0.00022124132167637516
        },
        {
          "timeFrame": "Sud America",
          "color": "Donald Trump",
          "freq": 21.9,
          "index": 13,
          "x": 182.55595244306502,
          "y": 189.62097108924766,
          "vy": 0.00003559659351961507,
          "vx": 0.0002645789697711447
        },
        {
          "timeFrame": "Sud America",
          "color": "Heat wave",
          "freq": 21.9,
          "index": 14,
          "x": 189.93199408611582,
          "y": 267.94477003987436,
          "vy": 0.00013285914311156585,
          "vx": -0.0000746047049267552
        },
        {
          "timeFrame": "Sud America",
          "color": "Asthma",
          "freq": 21.4,
          "index": 15,
          "x": 182.97147648076364,
          "y": 136.11188096843313,
          "vy": -0.000021630319723205723,
          "vx": -0.0002595939737966664
        },
        {
          "timeFrame": "Sud America",
          "color": "Greenhouse gas",
          "freq": 21.4,
          "index": 16,
          "x": 204.4022977590375,
          "y": 200.67614721986865,
          "vy": -0.000019374679676595605,
          "vx": -0.000011200373636411955
        },
        {
          "timeFrame": "Sud America",
          "color": "Greenpeace",
          "freq": 21.2,
          "index": 17,
          "x": 184.07220612407073,
          "y": 213.99889184844932,
          "vy": 0.00004960481670320061,
          "vx": 0.000027200769453671782
        },
        {
          "timeFrame": "Sud America",
          "color": "Jair Bolsonaro",
          "freq": 21.7,
          "index": 18,
          "x": 203.16109006060427,
          "y": 176.2821906958317,
          "vy": -0.000029205472824508403,
          "vx": 0.00016694030984948873
        },
        {
          "timeFrame": "Sud America",
          "color": "Gavin Newsom",
          "freq": 11.3,
          "index": 19,
          "x": 203.67894304717086,
          "y": 251.16639323965833,
          "vy": 0.000000684724506972551,
          "vx": -0.00023592408414786065
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Climate change",
          "freq": 86.7,
          "index": 20,
          "x": 322.1047376408532,
          "y": 180.86767813745018,
          "vy": -0.000019755169167727393,
          "vx": 0.0002680463713620922
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Global warming",
          "freq": 51.7,
          "index": 21,
          "x": 326.36701991926145,
          "y": 220.94508620897693,
          "vy": 0.0000010635720258903656,
          "vx": 0.00007229661596812174
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Greenhouse gas",
          "freq": 42.7,
          "index": 22,
          "x": 343.4069133966621,
          "y": 250.6008296808931,
          "vy": 0.00009233125706010915,
          "vx": -0.000465141264613036
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Donald Trump",
          "freq": 39.2,
          "index": 23,
          "x": 348.9533943836583,
          "y": 153.6036802688698,
          "vy": 0.000003353258529835879,
          "vx": 0.00010743117380966453
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Coronavirus",
          "freq": 22.5,
          "index": 24,
          "x": 356.37628095750375,
          "y": 224.87349536726376,
          "vy": 0.00021636787838558944,
          "vx": -0.00021865339550835864
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Intergovernmental Panel on Climate Change",
          "freq": 19.2,
          "index": 25,
          "x": 348.91249686637474,
          "y": 201.98423993503846,
          "vy": 0.00009672590929710767,
          "vx": 0.0001476237880146358
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Jair Bolsonaro",
          "freq": 18.8,
          "index": 26,
          "x": 356.12904545067624,
          "y": 179.9573846360826,
          "vy": 0.0000398848316701686,
          "vx": -0.000025868102223140868
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Scott Morrison",
          "freq": 18.6,
          "index": 27,
          "x": 315.64477045150255,
          "y": 248.2199532609473,
          "vy": -0.0002014547869016982,
          "vx": -0.00044000036727212104
        },
        {
          "timeFrame": "Medio Oriente",
          "color": "Jerry Brown",
          "freq": 18.4,
          "index": 28,
          "x": 322.56852535398986,
          "y": 146.94906081247402,
          "vy": -0.000021505888392201026,
          "vx": 0.00011362185478071012
        },
        {
          "timeFrame": "Australia",
          "color": "Bushfires in Australia",
          "freq": 89.4,
          "index": 29,
          "x": 464.5465146868178,
          "y": 192.62954611479466,
          "vy": 0.00001471599832497447,
          "vx": 0.00003428240251702747
        },
        {
          "timeFrame": "Australia",
          "color": "Meteorology",
          "freq": 34.5,
          "index": 30,
          "x": 467.3108751203343,
          "y": 230.25154423450078,
          "vy": 0.000005783495071556107,
          "vx": 0.0001558704177228545
        },
        {
          "timeFrame": "Australia",
          "color": "Climate change",
          "freq": 33.3,
          "index": 31,
          "x": 468.45953371225573,
          "y": 155.33757980152478,
          "vy": 0.000018182286984408968,
          "vx": 0.00006734926935817606
        },
        {
          "timeFrame": "Australia",
          "color": "Scott Morrison",
          "freq": 29.8,
          "index": 32,
          "x": 493.12966043616797,
          "y": 243.32137529893055,
          "vy": 0.00004632929481480715,
          "vx": -0.00003820819408568119
        },
        {
          "timeFrame": "Australia",
          "color": "Shane Fitzsimmons",
          "freq": 28.8,
          "index": 33,
          "x": 493.0875455852879,
          "y": 169.69846389759962,
          "vy": -0.00001717208630548129,
          "vx": -0.00011165511542159286
        },
        {
          "timeFrame": "Australia",
          "color": "Heat wave",
          "freq": 25.5,
          "index": 34,
          "x": 491.6025595054193,
          "y": 216.24530780884947,
          "vy": 0.00004694588496452593,
          "vx": -0.000057527131966372054
        },
        {
          "timeFrame": "Australia",
          "color": "Gladys Berejiklian",
          "freq": 19.8,
          "index": 35,
          "x": 471.0690157995491,
          "y": 256.69741050663254,
          "vy": 0.00003206101653993269,
          "vx": -0.00004704450755615086
        },
        {
          "timeFrame": "Australia",
          "color": "Firefighter",
          "freq": 15,
          "index": 36,
          "x": 491.6423338553399,
          "y": 145.4144495496668,
          "vy": -0.00002518050023300566,
          "vx": 0.000014476402260325024
        },
        {
          "timeFrame": "Australia",
          "color": "koala",
          "freq": 14.8,
          "index": 37,
          "x": 497.8106141228157,
          "y": 193.50442967911124,
          "vy": 0.0000041308149941253536,
          "vx": -0.00021436182806509375
        },
        {
          "timeFrame": "Russia",
          "color": "Climate change",
          "freq": 99.8,
          "index": 38,
          "x": 587.0411019585084,
          "y": 187.7952551215696,
          "vy": -0.000020542899074185056,
          "vx": 0.00022049805106379416
        },
        {
          "timeFrame": "Russia",
          "color": "Aerial Forest Protection Service",
          "freq": 90,
          "index": 39,
          "x": 647.7929947494189,
          "y": 138.90998733720693,
          "vy": -0.000035626437969656074,
          "vx": -0.0002128384637587492
        },
        {
          "timeFrame": "Russia",
          "color": "Permafrost",
          "freq": 90.5,
          "index": 40,
          "x": 627.5878730231259,
          "y": 295.36988344003026,
          "vy": 0.00002237448644833396,
          "vx": -0.00006559463142151784
        },
        {
          "timeFrame": "Russia",
          "color": "Greenpeace",
          "freq": 90.1,
          "index": 41,
          "x": 617.6277720435905,
          "y": 104.5010443467315,
          "vy": -0.0000851315582476257,
          "vx": 0.000043993442222414514
        },
        {
          "timeFrame": "Russia",
          "color": "Vladimir Putin",
          "freq": 87,
          "index": 42,
          "x": 620.1956585696946,
          "y": 220.40333639480974,
          "vy": 0.00006301916496347538,
          "vx": -0.000011923442366443683
        },
        {
          "timeFrame": "Russia",
          "color": "Donald Trump",
          "freq": 68.6,
          "index": 43,
          "x": 578.8453650966497,
          "y": 231.22808063759985,
          "vy": -0.00005712149337100598,
          "vx": 0.0000029326679587927258
        },
        {
          "timeFrame": "Russia",
          "color": "Global warming",
          "freq": 74.5,
          "index": 44,
          "x": 604.5567752968274,
          "y": 146.38019867640517,
          "vy": -0.0000414395287790441,
          "vx": 0.00018398077041675734
        },
        {
          "timeFrame": "Russia",
          "color": "Ilyushin Il-76",
          "freq": 73.6,
          "index": 45,
          "x": 645.7255431581275,
          "y": 255.49285211497275,
          "vy": 0.00013698164773903634,
          "vx": -0.00011289752149132694
        },
        {
          "timeFrame": "Russia",
          "color": "Greenhouse gas",
          "freq": 70.5,
          "index": 46,
          "x": 630.5549998868297,
          "y": 178.67775821732926,
          "vy": 0.00007301721547825808,
          "vx": 0.00003334552114275054
        },
        {
          "timeFrame": "Russia",
          "color": "NASA",
          "freq": 66.7,
          "index": 47,
          "x": 660.2251864549087,
          "y": 206.15636614705235,
          "vy": 0.00012616042810775842,
          "vx": -0.00002996027548390376
        },
        {
          "timeFrame": "Russia",
          "color": "Carbon dioxide",
          "freq": 59.5,
          "index": 48,
          "x": 606.0739545765028,
          "y": 259.4163321903518,
          "vy": 0.00003437955710474748,
          "vx": -0.0000917929691926957
        },
        {
          "timeFrame": "Asia",
          "color": "Climate change",
          "freq": 100,
          "index": 49,
          "x": 767.5569689560003,
          "y": 141.42019884441768,
          "vy": -0.0000980095010924115,
          "vx": -0.00008240739873079216
        },
        {
          "timeFrame": "Asia",
          "color": "Global warming",
          "freq": 60.8,
          "index": 50,
          "x": 774.2293413486527,
          "y": 236.79729807423274,
          "vy": 0.00016266351134719433,
          "vx": -0.00025732147597011496
        },
        {
          "timeFrame": "Asia",
          "color": "Palm oil",
          "freq": 50.2,
          "index": 51,
          "x": 747.5025213767166,
          "y": 211.5807048893494,
          "vy": -0.00008291840832414185,
          "vx": 0.00007901407679054492
        },
        {
          "timeFrame": "Asia",
          "color": "Greenhouse gas",
          "freq": 40,
          "index": 52,
          "x": 760.50703835412,
          "y": 180.70641702604604,
          "vy": -0.00004576487228237686,
          "vx": 0.00017457857239144874
        },
        {
          "timeFrame": "Asia",
          "color": "Deforestation",
          "freq": 32.4,
          "index": 53,
          "x": 756.68698515428,
          "y": 265.55597677622507,
          "vy": 0.000040632525885135474,
          "vx": -0.00002057887644478359
        },
        {
          "timeFrame": "Asia",
          "color": "Air pollution",
          "freq": 28.4,
          "index": 54,
          "x": 790.1439052430746,
          "y": 180.42142334218187,
          "vy": 0.00033473306841534005,
          "vx": 0.00017702308700100406
        },
        {
          "timeFrame": "Asia",
          "color": "Carbon dioxide",
          "freq": 26.7,
          "index": 55,
          "x": 777.6379384649572,
          "y": 204.45427450965352,
          "vy": 0.00017444088442840176,
          "vx": -0.00013101721297126506
        },
        {
          "timeFrame": "Asia",
          "color": "Coronavirus",
          "freq": 25.8,
          "index": 56,
          "x": 742.2860727495522,
          "y": 241.89695110318567,
          "vy": -0.0000639775677486301,
          "vx": 0.00015049151814532528
        },
        {
          "timeFrame": "Asia",
          "color": "Donald Trump",
          "freq": 22.4,
          "index": 57,
          "x": 732.596986512989,
          "y": 185.54530120974363,
          "vy": -0.00011687265970250794,
          "vx": 0.00016444490684200977
        },
        {
          "timeFrame": "Asia",
          "color": "Fossil fuel",
          "freq": 21.6,
          "index": 58,
          "x": 783.4050559701496,
          "y": 266.80478224256314,
          "vy": 0.00009095423924159153,
          "vx": -0.000021624180148841152
        },
        {
          "timeFrame": "Asia",
          "color": "koala",
          "freq": 17.3,
          "index": 59,
          "x": 739.9149195645969,
          "y": 163.14355535259807,
          "vy": -0.000024013188070926835,
          "vx": 0.00015608959481013004
        },
        {
          "timeFrame": "Europa",
          "color": "Climate change",
          "freq": 100,
          "index": 60,
          "x": 931.8814537685257,
          "y": 175.81846776395517,
          "vy": 0.000020812381074582012,
          "vx": -0.00032780813859299615
        },
        {
          "timeFrame": "Europa",
          "color": "Bushfires in Australia",
          "freq": 99.5,
          "index": 61,
          "x": 907.5700464345466,
          "y": 295.8214039698457,
          "vy": 0.00021251477132308778,
          "vx": -0.00020911888324437656
        },
        {
          "timeFrame": "Europa",
          "color": "Heat wave",
          "freq": 93,
          "index": 62,
          "x": 914.6888154814897,
          "y": 107.21891353680623,
          "vy": -0.000044482826825138194,
          "vx": -0.000044230482014135625
        },
        {
          "timeFrame": "Europa",
          "color": "Donald Trump",
          "freq": 86.9,
          "index": 63,
          "x": 916.6145834373942,
          "y": 219.74920693322957,
          "vy": 0.00018267756205971289,
          "vx": 0.00010170389398767882
        },
        {
          "timeFrame": "Europa",
          "color": "Scott Morrison",
          "freq": 71.5,
          "index": 64,
          "x": 891.0390864780807,
          "y": 254.45461550831132,
          "vy": 0.00012002262948087132,
          "vx": 0.000017726289855203915
        },
        {
          "timeFrame": "Europa",
          "color": "Global warming",
          "freq": 76,
          "index": 65,
          "x": 896.4984626338875,
          "y": 147.72244179079357,
          "vy": -0.0002052635013690081,
          "vx": -0.0000867733354895757
        },
        {
          "timeFrame": "Europa",
          "color": "Firefighters",
          "freq": 62.6,
          "index": 66,
          "x": 930.7710762938322,
          "y": 259.2011110945346,
          "vy": 0.00026336140582105394,
          "vx": -0.0001251813792722927
        },
        {
          "timeFrame": "Europa",
          "color": "koala",
          "freq": 59,
          "index": 67,
          "x": 873.296236821387,
          "y": 115.04413830824944,
          "vy": -0.00038094009351039444,
          "vx": 0.00015799439605702786
        },
        {
          "timeFrame": "Europa",
          "color": "Coronavirus",
          "freq": 60.1,
          "index": 68,
          "x": 890.4033059503386,
          "y": 187.49247119082966,
          "vy": -0.00011871614928205427,
          "vx": 0.00046463292124714945
        },
        {
          "timeFrame": "Europa",
          "color": "Deforestation",
          "freq": 28.2,
          "index": 69,
          "x": 872.1584680949237,
          "y": 283.0730676659526,
          "vy": 0.00013203184833143248,
          "vx": 0.000034902266700298374
        },
        {
          "timeFrame": "Europa",
          "color": "Greenhouse gas",
          "freq": 21.7,
          "index": 70,
          "x": 928.9484882767988,
          "y": 139.69015857054708,
          "vy": -0.000025608026562761505,
          "vx": -0.0000872109285348927
        },
        {
          "timeFrame": "Europa",
          "color": "Palm oil",
          "freq": 40.1,
          "index": 71,
          "x": 878.1585925359286,
          "y": 220.26651470664075,
          "vy": -0.0000847774496555845,
          "vx": 0.0005554724065636842
        },
        {
          "timeFrame": "Nord America",
          "color": "Climate change",
          "freq": 100,
          "index": 72,
          "x": 1073.0074648355371,
          "y": 198.46424363199537,
          "vy": 0.00004523342166738415,
          "vx": 0.00020061353072444834
        },
        {
          "timeFrame": "Nord America",
          "color": "National Weather Service",
          "freq": 97.1,
          "index": 73,
          "x": 1038.1530916459046,
          "y": 165.92110712008682,
          "vy": 0.00013222769370267663,
          "vx": 0.0003299871631150609
        },
        {
          "timeFrame": "Nord America",
          "color": "Global warming",
          "freq": 70.6,
          "index": 74,
          "x": 1040.2999116124615,
          "y": 273.9011101979324,
          "vy": -0.00016622120779565574,
          "vx": -0.00009827808460554402
        },
        {
          "timeFrame": "Nord America",
          "color": "Gavin Newsom",
          "freq": 67.3,
          "index": 75,
          "x": 1029.1431465961164,
          "y": 123.1325138006463,
          "vy": 0.00024958439070794453,
          "vx": -0.00020364915677381068
        },
        {
          "timeFrame": "Nord America",
          "color": "Donald Trump",
          "freq": 62.8,
          "index": 76,
          "x": 1062.2330242926455,
          "y": 240.54077966574854,
          "vy": -0.00003316716668582279,
          "vx": -0.00011411523326114696
        },
        {
          "timeFrame": "Nord America",
          "color": "Heat wave",
          "freq": 61.2,
          "index": 77,
          "x": 1023.6759726809988,
          "y": 237.85078161205712,
          "vy": -0.0001573119983913503,
          "vx": 0.00003268141869090417
        },
        {
          "timeFrame": "Nord America",
          "color": "Greenhouse gas",
          "freq": 54.7,
          "index": 78,
          "x": 1065.7857742249887,
          "y": 134.34243219105062,
          "vy": 0.00008188251108562029,
          "vx": -0.00014885660653818044
        },
        {
          "timeFrame": "Nord America",
          "color": "Coronavirus",
          "freq": 37.8,
          "index": 79,
          "x": 1076.2892069549757,
          "y": 272.55065141617007,
          "vy": -0.000005303382861386352,
          "vx": -0.00017172191007638077
        },
        {
          "timeFrame": "Nord America",
          "color": "Meteorology",
          "freq": 41.4,
          "index": 80,
          "x": 1022.3883567521242,
          "y": 202.5028477778892,
          "vy": -0.000031132696843346263,
          "vx": -0.00005132740482269844
        },
        {
          "timeFrame": "Nord America",
          "color": "Environment and Climate change Canada",
          "freq": 18.2,
          "index": 81,
          "x": 1073.1105994104562,
          "y": 163.0801046293359,
          "vy": 0.000016263483046269996,
          "vx": 0.00011975172379399522
        },
        {
          "timeFrame": "Nord America",
          "color": "Bobcat fire",
          "freq": 15.4,
          "index": 82,
          "x": 1010.5803919239955,
          "y": 264.6679458519342,
          "vy": -0.00018604917056423806,
          "vx": -0.00004119257850468901
        },
        {
          "timeFrame": "Nord America",
          "color": "NASA",
          "freq": 14.8,
          "index": 83,
          "x": 1055.390595356788,
          "y": 107.55444141810071,
          "vy": 0.00021261243863124565,
          "vx": -0.0005124361512514401
        },
        {
          "timeFrame": "Nord America",
          "color": "Joe Biden",
          "freq": 13.7,
          "index": 84,
          "x": 1044.3328617438508,
          "y": 216.99575301715538,
          "vy": -0.0001572005044794855,
          "vx": 0.00003193265645595696
        }
      ]
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.createBubbleChart();
      window.addEventListener('resize', this.createBubbleChart); // Recreate chart on window resize
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.createBubbleChart);
  },
  methods: {
    createBubbleChart() {
      // Remove any existing SVG before creating a new one
      d3v5.select(this.$refs.bubbleChart).selectAll('*').remove();

      const bubbleData = this.rawdata;
      const word = 'color';
      const frequency = 'freq';
      const maxSize = 22;
      const xAxis = 'timeFrame';

      const container = this.$refs.bubbleChartContainer;
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;
      const width = containerWidth;
      const height = containerHeight;
      console.log('height', height);
      console.log('width', width);
      const margin = { t: 0, l: 50, r: 20, b: 0 };
      const padding = 2;

      if (xAxis === undefined) {
        bubbleData.map(d => (d.xAxis = 0));
      }

      const time = d3v5.set(bubbleData.map(d => d[xAxis])).values();

      let x = d3v5
        .scalePoint()
        .domain(time)
        .range([margin.l, width - margin.l - margin.r]);

      let svg = d3v5
        .select(this.$refs.bubbleChart)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      const xaxis = svg
        .append("g")
        .attr("transform", `translate(0,${height - 50})`)
        .call(d3v5.axisBottom(x));

      const colorScale = d3v5.scaleOrdinal(d3v5.schemeCategory10);

      const luminance = 50;
      const textColor = d3v5
        .scaleQuantile()
        .range(["#fff", "#000"])
        .domain([0, luminance, 100]);

      const r = d3v5
        .scaleSqrt()
        .domain([0, d3v5.max(bubbleData, d => d[frequency])])
        .range([0, maxSize]);

      const simulation = d3v5
        .forceSimulation(bubbleData)
        .force("x", d3v5.forceX(d => x(d[xAxis])).strength(1))
        .force("y", d3v5.forceY(height / 2).strength(0.2))
        .force(
          "collide",
          d3v5
            .forceCollide()
            .radius(d => r(d[frequency]) + padding)
            .iterations(10)
        )
        .alpha(0.2);

      let gBubble = svg.selectAll('gBubble').data(bubbleData);
      gBubble.exit().remove();

      let bubble = gBubble
        .enter()
        .append('g')
        .classed('gBubble', true)
        .attr('id', d => d[word]);

      bubble
        .append('circle')
        .attr('r', d => r(d[frequency]))
        .attr('fill', d => colorScale(d[word]))
        .attr('fill-opacity', 0.4)
        .attr('stroke', d => d3v5.rgb(colorScale(d[word])).darker(1))
        .attr('stroke-width', 1);

      const textLabels = bubble
        .append('text')
        .text(d => d[word])
        .style('text-anchor', 'middle')
        .attr("dominant-baseline", "central")
        .attr('font-family', 'sans-serif')
        .attr('font-size', '8px')
        .attr('font-weight', 'normal')
        .style('stroke', 'white')
        .style('stroke-width', 2);

      const textBck = bubble
        .append('text')
        .text(d => d[word])
        .style('text-anchor', 'middle')
        .attr("dominant-baseline", "central")
        .attr('font-family', 'sans-serif')
        .attr('font-size', '8px')
        .attr('font-weight', 'normal');

      gBubble = gBubble.merge(bubble);

      gBubble.call(this.drag(simulation));

      simulation.nodes(bubbleData).on('tick', () => {
        gBubble.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');
      });
    },
    drag(simulation) {
      function dragstarted(d) {
        if (!d3v5.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3v5.event.x;
        d.fy = d3v5.event.y;
      }

      function dragended(d) {
        if (!d3v5.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      return d3v5
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  }
};
</script>

<style scoped>
.bubble-chart-container {
  width: 100%;
  height: 100%;
}
</style>