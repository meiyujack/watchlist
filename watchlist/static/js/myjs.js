$(document).ready(function () {
    $("textarea").hide();
    $("#btn").click(function () {
        var so = $(".somatization");
        var oc = $(".oc");
        var se = $(".sensitive");
        var de = $(".depression");
        var an = $(".anxiety");
        var ho = $(".hostile");
        var te = $(".terrified");
        var pa = $(".paranoid");
        var s = $(".s");
        var ot = $(".others");
        var names=['躯体化','强迫症状','人际关系敏感','抑郁症状','焦虑症状',
            '敌对症状','恐怖症状','偏执症状','精神症状','饮食睡眠'];
        var scores = new Array(10);
        for (var t = 0; t < scores.length; t++) {
            scores[t] = 0;
        }
        var total = [so, oc, se, de, an, ho, te, pa, s, ot];
        t=0;
        var c,sum=0;
        for (var item of total) {
            for (var i of item) {
                if (i.checked) {
                    if( parseInt(i.value)>=2) {
                        c++;
                    }
                    scores[t] += parseInt(i.value);
                }
            }
            t++;
        }
        for (var sc=0;sc<scores.length;sc++)
        {
            sum+=scores[sc];
            names[sc]=names[sc]+'：'+scores[sc]+'\r\n'
        }
        $("textarea").html(names).show();
    });
});
