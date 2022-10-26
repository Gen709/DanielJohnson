// https://codepen.io/palimondo/pen/KQpVXK
// https://community.plotly.com/t/color-a-group-of-individual-points-in-boxplot/10432

$(document).ready(function() {
    var student_id = $("input[name=student_id]").val();
//    console.log(student_id)
    $.ajax({
        type: "POST",
        dataType: "json",
		url: "http://127.0.0.1:8000/etudiant/ajax/notes/",
        data:{student_id: student_id},
        success: function(data){
            var xData = []
            var yData = []
            var studentGradeIndex = []

            $.each(data["class_grades"], function(className, values){
                xData.push(className);
                yData.push(values);
//                get the index
                console.log(className)
                var classNameIndex = data["class_name_list"].indexOf(className);
                studentGradeIndex.push(values.indexOf(data["grade_list"][classNameIndex]));
            });
//            console.log(data["grade_list"], data["class_name_list"], data["class_grades"]);

//            var colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)'];


            var trace1 = [];
//            var trace2 = [];

            for ( var i = 0; i < xData.length; i ++ ) {
                var result = {
                    type: 'box',
                    y: yData[i],
                    name: xData[i],
                    boxpoints: 'all',
                    selectedpoints: [studentGradeIndex[i]],
                    jitter: 0.5,
                    whiskerwidth: 0.2,
                    fillcolor: 'cls',
                    marker: {
                        size: 4
                    },
                    line: {
                        width: 1
                    }
                };
                trace1.push(result);
            };

            var trace2 = {
                x: data["class_name_list"],
                y: data["grade_list"],
                mode: 'markers',
//                type:"bar",
//                name: 'steepest',
//                line: {color: 'black'},
//                type: 'scatter'
            };

            layout = {
                title: "Portrait académique",
                xaxis: {
                    type: 'category',
                    title: 'Matière',
                },
                yaxis: {
                    autorange: true,
                    showgrid: true,
                    zeroline: true,
                    dtick: 5,
                    gridcolor: 'rgb(255, 255, 255)',
                    gridwidth: 1,
                    zerolinecolor: 'rgb(255, 255, 255)',
                    zerolinewidth: 2
                },
                margin: {
                    l: 40,
                    r: 30,
                    b: 80,
                    t: 100
                },
//                paper_bgcolor: 'rgb(243, 243, 243)',
//                plot_bgcolor: 'rgb(243, 243, 243)',
                showlegend: false
            };

            test = [trace1, trace2];

            Plotly.newPlot('myDiv', trace1, layout);

        }
    });
});


