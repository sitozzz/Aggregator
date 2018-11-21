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
    function showSdekResults(data) {
        console.log(data);
        // console.log(data['result']);
        if (data != undefined) {
            // data = data['result'];
            // console.log(data);
            let price = data['price'];
            let deliveryPeriodMin = data['deliveryPeriodMin'];
            let deliveryPeriodMax = data['deliveryPeriodMax'];
            let deliveryDateMin = data['deliveryDateMin'];
            let deliveryDateMax = data['deliveryDateMax'];
            document.getElementById('priceSDEK').innerText = price + ' Rub';
            document.getElementById('errorSDEK').innerText = '';
            // $('#priceSDEK').val(price + ' Rub');
        } else {
            console.log(data);
            // data = data.error[0];
            document.getElementById('priceSDEK').innerText ='';
            document.getElementById('errorSDEK').innerText ="Доставка невозможна при заданных условиях";
        }
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
                'tariffName': $('#tariff').find(':selected').text(),
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
                // TODO: Only for sdek api!
                 showSdekResults(data.sdek.result)
                
                $('#output').show('fast');
            }
        });
    });
    function getTariffs() {
        $.ajax({
            url : "/get_tariffs",
            contentType: 'application/json',
            method : 'GET',
            success : function(data) {
                data = data['fields'];
                var tariffHolder = document.getElementById('tariff');
                for(let elem in data){
                    if (data[elem] != '') {
                        console.log(data[elem]);
                        let option = document.createElement('option');
                        option.id = 'option-' + elem;
                        option.text = data[elem];
                        tariffHolder.appendChild(option);
                    }
                    
                }
            }
        });
    }
    getTariffs();
    
  
});