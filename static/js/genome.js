//draw choromosome parm qarm base on the json from url
var chr_pq_arm = function(_d,_url,_chrlen){
    $(_d).css("display","inline");

    $.getJSON(_url,function(data){
        console.log("ok");
        var chrnum=0;
        $.each(data,function(idx,item) {
            console.log(idx, chrnum, item && item.armratio);
            if (idx == "num") {
                chrnum = item;
            }
            else {

                $(_d).append(
                    "<li> <a href='www.baidu.com' > <p>" + idx + "</p> <span class='  "+ idx +"  parm'></span> <span class='" + idx + " qarm'></span> </a> </li>"
                );
                var armratio=parseFloat(item.armratio);
                var chrlen=parseFloat(_chrlen);

                var parmlen=(1.0/(1.0+armratio)*chrlen);
                var qarmlen=(armratio/(1.0+armratio)*chrlen);

                $("."+idx+".parm").css("height",  parmlen+'em');
                $("."+idx+".qarm").css("height",  qarmlen+'em');

            }
            //$(d +":lastChild").css("")
        });
    });
};