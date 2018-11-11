$(document).ready(function () {
    //This sends to server
    //City object
    function City(id, name) {
        this._id = id;
        this._name = name;
    }
    //Delivery data
    function DeliveryData( weight, length, height, width) {
        this.weight = weight;
        this.length = length;
        this.height = height;
        this.width = width;
        //this.size = height*width*length;
    }
    var city1;
    var city2;
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
            city1 = new City(ui.item.id, ui.item.value);
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
            city2 = new City(ui.item.id, ui.item.value);
        }
    });
    $("#calcBtn1").click(function (){
        $("#prop-holder").show(100);
    });
    $("#calcBtn").click(function () {
        
        //Collect data from fields
        let deliveryData = new DeliveryData(
          
            $('#weight').val(), 
            $('#length').val(),
            $('#height').val(),
            $('#width').val()
        );
        $.ajax({
            url : "/calculate",
            contentType: 'application/json',
            method: 'POST',
            data : JSON.stringify({
                'city1': {
                    'id': city1._id,
                    'name': city1._name,
                },
                'city2': {
                    'id': city2._id,
                    'name': city2._name,
                }, 
                'dateExecute':  $('#dateExecute').val(),
                //1 or more
                //TODO: Example hardcode!!!
                'goods':[
                    {
                        'weight': deliveryData.weight,
                        'height': deliveryData.height,
                        'width': deliveryData.width,
                        'length': deliveryData.length
                    }
                ]
            }),
            success : function(data) {
                // TODO: show result
                console.log('RESPONSE FROM FLASK:');
                console.log(data);
            }
        });
    });
});