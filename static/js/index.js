var city1;
var city2;
var deliveryDataFrom = 'door';
var deliveryDataTo = 'door';
var d = document;

//This sends to server
//City object
function City(id, name) {
    this._id = id;
    this._name = name;
}
//Delivery data
function DeliveryData(weight, length, height, width, size) {
    if (size == undefined) {
        this.weight = weight;
        this.length = length;
        this.height = height;
        this.width = width;
    } else {
        this.weight = weight;
        this.size = size;
    }
}


function showResults(data) {
    showDPDres(data.dpd);
    showPonyres(data.pony);
    showBoxberry(data.boxberry);
    showSDEKres(data.sdek);
}

function showSDEKres(sdekdata) {
    console.log('sdek data');
    console.log(sdekdata);
    $('#sdek-output').html('');
    // TODO: Change tariff id to tariff name from this dict
    let tariff_map = {

    };
    if (sdekdata.error == undefined) {

        data = sdekdata.result;
        console.log(data);
        if (data != undefined) {
            let price = data['price'];
            let deliveryPeriodMin = data['deliveryPeriodMin'];
            let deliveryPeriodMax = data['deliveryPeriodMax'];
            let deliveryDateMin = data['deliveryDateMin'];
            let deliveryDateMax = data['deliveryDateMax'];
            let tariffName = data['tariffId'];

            var sdekHolder = d.getElementById('dpd-output');
            var row = d.createElement('div')
            row.className = 'row';
            row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
            sdekHolder.appendChild(row);
            var title = d.createElement('h1');
            title.innerText = 'SDEK';
            row.appendChild(title);
            var propHolder = d.createElement('div');
            propHolder.style = 'width:100%';
            propHolder.innerHTML = '<p>' + price + ' Rub </p><p>Дата доставки: ' + deliveryDateMax + '</p><p>Тариф: '+tariffName+'</p>';
            row.appendChild(propHolder);

        } 
    }
}

function showDPDres(dpdData) {
    $('#dpd-output').html('');
    if (dpdData[0].serviceName) {
        var dpdHolder = d.getElementById('dpd-output');
        var row = d.createElement('div')
        row.className = 'row';
        row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        dpdHolder.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = 'Стоимость доставки DPD';
        row.appendChild(title);
        for (let r in dpdData) {
            var propHolder = d.createElement('div');
            propHolder.style = 'width:100%;';
            propHolder.innerHTML = '<p> услуга: ' + dpdData[r].serviceName + ', цена: ' + dpdData[r].cost + ' дней до доставки: ' + dpdData[r].days + '</p>'
            row.appendChild(propHolder);
        }
    } else {
        var dpdHolder = d.getElementById('dpd-output');
        var row = d.createElement('div')
        row.className = 'row';
        row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        dpdHolder.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = dpdData.replace('Server raised fault: ', '');
        row.appendChild(title);

    }

    $('#dpd-output').show();
}
function showPonyres(ponyData) {
    $('#pony-output').html('');
    $('#pony-output').show();
    let row = d.createElement('div')
    let title = d.createElement('h1');
    title.innerText = 'Pony Express';
    row.appendChild(title);
    row.className = 'row';
    row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
    


    for (let i in ponyData) {

        var propHolder = d.createElement('div');
        propHolder.style = 'width:100%;';
        propHolder.innerHTML = '<p> услуга: ' + ponyData[i].Mode + ', цена без НДС: ' + ponyData[i].Sum + ' НДС: ' + ponyData[i].VAT + ' дней до доставки: ' + ponyData[i].MaxTerm + '</p>'
        row.appendChild(propHolder);
    }
    $('#pony-output').append(row);
    //----------------------------------------

   


}

function showBoxberry(boxberryData) {
    console.log(boxberryData);
    $('#boxberry-output').html('');
    if (boxberryData.price) {
        var blockBoxberry = d.getElementById('boxberry-output');
        console.log(blockBoxberry);
        var row = d.createElement('div');
        row.className = 'row';
        row.style = "margin: auto; padding: 0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        blockBoxberry.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = 'Стоимость доставки Boxberry';
        row.appendChild(title);
        var deliveryInformation = d.createElement('div');
        deliveryInformation.style = 'width: 100%;';
        deliveryInformation.innerHTML = '<p> Цена: ' + boxberryData.price + '; дней до доставки: ' + boxberryData.period + '</p>';
        row.appendChild(deliveryInformation);
    }
    
    $('#boxberry-output').show();
}

$(document).ready(function () {
    d.getElementById('dateExecute').value = new Date().toISOString().slice(0,10);
    $('input[name=fromDelivery]').on('change', function () {
        deliveryDataFrom = $(this).val();
    });
    $('input[name=toDelivery]').on('change', function () {
        deliveryDataTo = $(this).val();
    });
    $('input[name=calcVariant]').on('change', function () {
        if ($(this).val() == 'variant1') {
            $('#variant1').show();
            $('#variant2').hide();
        } else {
            $('#variant1').hide();
            $('#variant2').show();
        }

    });
    $("#city1").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType: "jsonp",
                data: {
                    q: function () {
                        return $("#city1").val()
                    },
                    name_startsWith: function () {
                        return $("#city1").val()
                    }
                },
                success: function (data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function (item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            city1 = new City(ui.item.id, ui.item.value);
        }
    });
    $("#city2").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType: "jsonp",
                data: {
                    q: function () {
                        return $("#city2").val()
                    },
                    name_startsWith: function () {
                        return $("#city2").val()
                    }
                },
                success: function (data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function (item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            city2 = new City(ui.item.id, ui.item.value);
        }
    });
    $("#calcBtn1").click(function () {
        $("#prop-holder").show(100);
    });
    $("#calcBtn").click(function () {

        //Collect data from fields
        let size;
        if ($('#variant2').is(':visible')) {
            size = $('#size').val();
        }
        let deliveryData = new DeliveryData(

            $('#weight').val(),
            $('#length').val(),
            $('#height').val(),
            $('#width').val(),
            size
        );
        console.log('Delivery data = ');
        console.log(deliveryData);

        // TODO: Show loader here!
        $.ajax({
            url: "/calculate",
            contentType: 'application/json',
            method: 'POST',
            data: JSON.stringify({
                'city1': {
                    'id': city1._id,
                    'name': city1._name,
                },
                'city2': {
                    'id': city2._id,
                    'name': city2._name,
                },
                'dateExecute': $('#dateExecute').val(),
                // 'tariffName': $('#tariff').find(':selected').text(),

                //Door to door, door to storage and other 
                'deliveryType': {
                    'deliveryFrom': deliveryDataFrom,
                    'deliveryTo': deliveryDataTo
                },

                //TODO: Example hardcode!!!
                'goods': [
                    {
                        'weight': deliveryData.weight,
                        'height': deliveryData.height,
                        'width': deliveryData.width,
                        'length': deliveryData.length,
                        'volume': deliveryData.size
                    }
                ]
            }),
            success: function (data) {
                // TODO: Hide loader here!
                console.log(data);

                showResults(data)

                $('#output').show('fast');
            }
        });
    });
});