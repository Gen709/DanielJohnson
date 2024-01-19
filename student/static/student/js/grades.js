// https://codepen.io/palimondo/pen/KQpVXK
// https://community.plotly.com/t/color-a-group-of-individual-points-in-boxplot/10432

$(document).ready(function() {
    var student_id = $("input[name=student_id]").val();
    

    // Get the semester value from the initially active carousel item
    var initialSemester = $('.carousel-item.active').find('.row#semester_number').attr('value');
    console.log("initial semester", initialSemester)
    var layout = {
                    xaxis: {
                        type: 'category',
                        title: 'Matière',
                    },
                    yaxis: {
                        // autorange: false,
                        showgrid: true,
                        // zeroline: true,
                        // dtick: 10,
                        // range: [0, 100],
                        gridcolor: 'rgb(255, 255, 255)',
                        gridwidth: 1,
                        zerolinecolor: 'rgb(255, 255, 255)',
                        zerolinewidth: 2
                    },
                    margin: {
                        l: 40,
                        r: 30,
                        b: 80,
                        t: 80
                    },
                    showlegend: false
                };
        
    // Perform the initial AJAX call with both student_id and the initially active semester
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "http://127.0.0.1:8000/etudiant/ajax/notes/",
        data: {
            student_id: student_id,
            semester: initialSemester
        },
        success: function(data) {
            var xData = [];
            var yData = [];
            var studentGradeIndex = [];

            $.each(data["class_grades"], function(className, values) {
                xData.push(className);
                yData.push(values);
                // get the index
                var classNameIndex = data["class_name_list"].indexOf(className);
                studentGradeIndex.push(values.indexOf(data["grade_list"][classNameIndex]));
            });

            var trace1 = [];
            for (var i = 0; i < xData.length; i++) {
                var result = {
                    type: 'box',
                    y: yData[i],
                    name: xData[i],
                    boxpoints: 'all',
                    selectedpoints: [studentGradeIndex[i]],
                    jitter: 0.3,
                    whiskerwidth: 0.2,
                    fillcolor: 'cls',
                    marker: {
                        size: 8,
                    },
                    line: {
                        width: 1
                    }
                };

                trace1.push(result);
            }

            // var trace2 = {
            //     x: data["class_name_list"],
            //     y: data["grade_list"],
            //     mode: 'markers',
            //     marker: {
            //         size: 8,
            //     },
            // };
            Plotly.newPlot('myDiv', trace1, layout);
        },
        error: function(error) {
            console.error("AJAX Error:", error);
        }
    });

    // Event handler for Bootstrap Carousel slide event
    $('#carouselExampleIndicators').on('slid.bs.carousel', function() {
        // Get the active carousel item
        var activeItem = $('.carousel-item.active');

        // Get the semester value from the active carousel item
        var semesterOfActiveWindow = activeItem.find('.row#semester_number').attr('value');
        console.log("semester update", semesterOfActiveWindow)
        // Perform the AJAX call with both student_id and the active semester
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "http://127.0.0.1:8000/etudiant/ajax/notes/",
            data: {
                student_id: student_id,
                semester: semesterOfActiveWindow
            },
            success: function(data) {
                console.log("AJAX success on carousel change:", data);
                var xData = [];
                var yData = [];
                var studentGradeIndex = [];

                $.each(data["class_grades"], function(className, values) {
                    xData.push(className);
                    yData.push(values);
                    // get the index
                    var classNameIndex = data["class_name_list"].indexOf(className);
                    studentGradeIndex.push(values.indexOf(data["grade_list"][classNameIndex]));
                });

                var trace1 = [];
                for (var i = 0; i < xData.length; i++) {
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
                            size: 6,
                        },
                        line: {
                            width: 1
                        }
                    };

                    trace1.push(result);
                }

                // var trace2 = {
                //     x: data["class_name_list"],
                //     y: data["grade_list"],
                //     mode: 'markers',
                // };

                // Update the Plotly chart with the new data
                Plotly.newPlot('myDiv', trace1, layout);
            },
            error: function(error) {
                console.error("AJAX Error:", error);
            }
        });
    });
});


