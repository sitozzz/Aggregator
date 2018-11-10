$(document).ready(function () {
    //This sends to server
    var city1Id;
    var city2Id;
    $("#city1").autocomplete({
        source : function(request, response) {
            $.ajax({
                url : "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType : "jsonp",
                data : {
                    q : function() {
                        return $("#city1").val()
                    },
                    name_startsWith : function() {
                        return $("#city1").val()
                    }
                },
                success : function(data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function(item) {
                        return {
                            label : item.name,
                            value : item.name,
                            id : item.id
                        }
                    }));
                }
            });
        },
        minLength : 1,
        select : function(event, ui) {
            //console.log("Yep!");
            console.log('Selected id = ', ui.item.id);
            city1Id = ui.item.id;
            // $('#receiverCityId').val(ui.item.id);
        }
    });

    $("#city2").autocomplete({
        source : function(request, response) {
            $.ajax({
                url : "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType : "jsonp",
                data : {
                    q : function() {
                        return $("#city2").val()
                    },
                    name_startsWith : function() {
                        return $("#city2").val()
                    }
                },
                success : function(data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function(item) {
                        return {
                            label : item.name,
                            value : item.name,
                            id : item.id
                        }
                    }));
                }
            });
        },
        minLength : 1,
        select : function(event, ui) {
            //console.log("Yep!");
            console.log('Selected id = ', ui.item.id);
            city2Id = ui.item.id;
            // $('#receiverCityId').val(ui.item.id);
        }
    });
});