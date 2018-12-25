var city1;
var city2;
var deliveryDataFrom = 'door';
var deliveryDataTo = 'door';
var d = document;

function* entries(obj) {
    for (let key of Object.keys(obj)) {
        yield [key, obj[key]];
    }
}

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
// ===SDEK FUNCTIONS===
function showSDEKres(sdekdata) {
    console.log('sdek data');
    console.log(sdekdata);
    $('#sdek-output').html('');
    let tariff_map = {
        136: 'Посылка',
        137: 'Посылка',
        138: 'Посылка',
        139: 'Посылка',
        233: 'Экономичная посылка',
        234: 'Экономичная посылка',
        291: 'Express',
        293: 'Express',
        294: 'Express',
        295: 'Express',
        1: 'Экспресс лайт',
        5: 'Экономичный экспресс',
        3: 'Супер-экспресс до 18',
        10: 'Экспресс лайт',
        11: 'Экспресс лайт',
        12: 'Экспресс лайт',
        15: 'Экспресс тяжеловесы',
        16: 'Экспресс тяжеловесы',
        17: 'Экспресс тяжеловесы',
        18: 'Экспресс тяжеловесы',
        62: 'Магистральный экспресс',
        63: 'Магистральный экспресс',
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

            for (let [key, value] of entries(tariff_map)) {
                if (key == tariffName) {
                    tariffName = value;
                }
            }

            var sdekHolder = d.getElementById('sdek-output');
            var row = d.createElement('div')
            row.className = 'row';
            row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
            sdekHolder.appendChild(row);
            var title = d.createElement('h1');
            title.innerText = 'SDEK';
            row.appendChild(title);
            var propHolder = d.createElement('div');
            propHolder.style = 'width:100%';
            propHolder.innerHTML = '<p>' + price + ' Rub </p><p>Дата доставки: ' + deliveryDateMax + '</p><p>Тариф: ' + tariffName + '</p>';
            row.appendChild(propHolder);
            var btn = d.createElement('button');
            btn.className = 'btn btn-lg btn-success';
            btn.innerText = 'Заказать';
            row.appendChild(btn);

            btn.onclick = function () {
                if (deliveryDataFrom != 'door') {
                    $("#send-door").hide();
                    $("#send-storage").show();
                    getSDEKPvz(city1._id, 'sdek-dropdown-from');
                    // TODO: display full address in p tag
                }
                if (deliveryDataTo != 'door') {
                    $("#recieve-door").hide();
                    $("#recieve-storage").show();
                    getSDEKPvz(city2._id, 'sdek-dropdown-to');
                    // TODO: display full address in p tag
                }
                $('.section').fadeOut('fast', function () {
                    d.getElementById('send-city').innerText = $('#city1').val();
                    d.getElementById('recieve-city').innerText = $('#city2').val();

                    $('#order').fadeIn('fast');
                });


            };

            // var dropdownContainer = d.createElement('div');
            // dropdownContainer.id = 'drop-container';
            // dropdownContainer.style = 'display:none';
            // dropdownContainer.className = '';

            // var dropdownTo = d.createElement('select');
            // dropdownTo.id = 'sdek-dropdown-to';
            // dropdownTo.className = 'form-control';
            // var dropdownLabelTo = d.createElement('p');
            // dropdownLabelTo.innerText = 'Выберите пункт отправления из списка: ';
            // dropdownContainer.appendChild(dropdownLabelTo);
            // dropdownContainer.appendChild(dropdownTo);

            // var dropdown = d.createElement('select');
            // dropdown.id = 'sdek-dropdown';

            // dropdown.className = 'form-control';
            // var dropdownLabel = d.createElement('p');
            // dropdownLabel.innerText = 'Выберите пункт получения из списка: ';

            // dropdownContainer.appendChild(dropdownLabel);
            // dropdownContainer.appendChild(dropdown);
            // row.appendChild(dropdownContainer);


            // var fullAddressText = d.createElement('p');
            // fullAddressText.id = 'full-address-text';
            // row.appendChild(fullAddressText);

            $(sdekHolder).show();

        }
    }
}

function getSDEKPvz(city_code, rootElement) {
    console.log('CITY CODE  = ' + city_code);
    $.ajax({
        contentType: 'application/json',
        method: 'POST',
        url: "/sdek_pvz",
        data: JSON.stringify({
            "city_code": city_code
        }),

        success: function (response) {
            //TODO: Display dropdown and some info here
            console.log('Success sdek pvz');
            console.log(response);

            for (let elem in response) {
                createSDEKDropdown(response[elem], rootElement);
            }

            $('#drop-container').show();
            // $('#sdek-dropdown').on('change', function (e) {
            //    d.getElementById('full-address-text').innerText = 'Адрес ПВЗ получателя: ' + $('option:selected', this).val();
            // });
        },
        error: function (err) {
            console.log('AJAX ERROR');
            console.log(err);
        }

    });

}

function createSDEKDropdown(data, rootElement) {
    var root = d.getElementById(rootElement);
    var option = d.createElement('option');
    option.id = data['code'];
    option.innerText = data['display_name'];
    option.value = data['full_address'];
    root.appendChild(option);
}

function addSDEKDelivery(isSendStorage, isRecieveStorage) {
    var dateDelivery = new Date().toJSON().slice(0, 10);
    var sender = {
        'city_id': city1._id,
        'phone': $('#send-phone').text(),
        'name': $('#send-name').text()
    };
    var reciever = {
        'city_id': city2._id,
        'phone': $('#reciever-phone').text(),
        'name': $('#reciever-name').text()
    };
    var package = {
        'height': $('#height').val(),
        'width': $('#width').val(),
        'weight': $('#weight').val(),
        'length': $('#length').val()
    };
    if (isSendStorage) {
        // TODO: Add fields for storage
    } else {
        sender['street'] = $('#send-street').text();
        sender['flat'] = $('#send-flat').text();
        sender['house'] = $('#send-house').text();
    }

    if (isRecieveStorage) {
        // TODO: Add fields for storage
    } else {
        reciever['street'] = $('#recieve-street').text();
        reciever['flat'] = $('#recieve-flat').text();
        reciever['house'] = $('#recieve-house').text();
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",

        url: "/sdek_delivery",
        data: JSON.stringify({
            'date': dateDelivery,
            'sender': sender,
            'reciever': reciever,
            package: package
        }),
        success: function (response) {
            console.log('response = ' + response);
        }
    });
}

// ===SDEK FUNCTIONS===

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
    d.getElementById('dateExecute').value = new Date().toISOString().slice(0, 10);
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
        $('#loader').show();
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
                $('#loader').hide();
                console.log(data);

                showResults(data)

                $('#output').show('fast');
            }
        });
    });
    $("#close-sdek-order").click(function () {
        $("#order").fadeOut('fast', function () { $(".section").fadeIn('fast'); });
    });

    $('#sdekOrderBtn').click(function () { 
        // TODO: check this flags after user selection
        addSDEKDelivery(false, false);
        
    });
});