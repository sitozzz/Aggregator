// Название перевозщика
// Звезды
// Дата отправки
// Дата приема 
// Цена 
// function showResults(data) {
//     data = [
//         {
//             name: 'sdek',
//             shippingDate: '21',
//             receivingDate: '23',
//             price: 2767,
//         },
//         {
//             name: 'dek',
//             shippingDate: '23',
//             receivingDate: '23',
//             price: 27267,
//         },
//         {
//             name: 'mek',
//             shippingDate: '23',
//             receivingDate: '27',
//             price: 27167,
//         }
//     ]
//     for (const carrier of data) {
//         showCarrier(carrier)
//     }
// }

// function showCarrier({name, shippingDate, receivingDate, price}) {
//     const container = d.createElement('div')
//     container.setAttribute('class', 'carrier')
    
//     const nameElement  = d.createElement('div')
//     nameElement.setAttribute('class', 'carrier-name')
//     nameElement.textContent = name

//     const shippingDateElement  = d.createElement('div')
//     shippingDateElement.setAttribute('class', 'carrier-shipping-date')
//     shippingDateElement.textContent = shippingDate

//     const receivingDateElement  = d.createElement('div')
//     receivingDateElement.setAttribute('class', 'carrier-receiving-date')
//     receivingDateElement.textContent = receivingDate

//     const priceElement  = d.createElement('div')
//     priceElement.setAttribute('class', 'carrier-price')
//     priceElement.textContent = price

//     container.appendChild(nameElement)
//     container.appendChild(shippingDateElement)
//     container.appendChild(receivingDateElement)
//     container.appendChild(priceElement)

//     d.getElementById('shipping-offers').appendChild(container)
// }
var city1;
var city2;
var deliveryDataFrom = 'door';
var deliveryDataTo = 'door';
var d = document;

//var sdekFunc = 
//prepareSdekOrder

function dpdOrdPrev(data) {
    
    if (deliveryDataFrom != 'door') {
        $("#send-door").hide();
        $("#send-storage").show();
        // getSDEKPvz(city1._id, 'sdek-dropdown-from');
        // // TODO: display full address in p tag
    }
    if (deliveryDataTo != 'door') {
        $("#recieve-door").hide();
        $("#recieve-storage").show();
        // getSDEKPvz(city2._id, 'sdek-dropdown-to');
        // // TODO: display full address in p tag
    }
    $('#calc').fadeOut('fast', function () {
        d.getElementById('dpd-send-city').innerText = $('#city1').val();
        d.getElementById('dpd-recieve-city').innerText = $('#city2').val();
        $('#dpd-order').fadeIn('fast');
    });
}


var respGlob = {
    "cdek": {
        'func': prepareSdekOrder, 
        'data': undefined
    },
    "dpd": {
        'func': dpdOrdPrev, 
        'data': undefined
    },
    "boxberry": { 'func': undefined, 'data': undefined },
    "pony": { 'func': undefined, 'data': undefined },
};


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

// Название перевозщика
// Звезды
// Дата отправки
// Дата приема 
// Цена 
function showResults(data) {
    // data = [
    //     {
    //         name: 'cdek',
    //         shippingDate: 1547906646,
    //         receivingDate: 1547906646,
    //         price: 2767,
    //     },
    //     {
    //         name: 'dpd',
    //         shippingDate: 1547906646,
    //         receivingDate: 1547906646,
    //         price: 27267,
    //     },
    // ]
    d.getElementById('shipping-offers').innerHTML = '';
   

    prArr = []
    for (var carrier in data) {
        for (var i in data[carrier]) {
            
               prArr.push({'carrier':carrier,'price':data[carrier][i].price})
            
 
        }
    }
    var sorted = true;
    console.log(prArr);
    while (sorted) {
        
        sorted = false;
        for (var el=0; el< prArr.length-1; el++) {
            if (prArr[el].price > prArr[el+1].price){
                console.log('enter if ');
                var cup = prArr[el];
                prArr[el] = prArr[el+1];
                prArr[el+1] = cup;
                sorted = true;
            }
        }
        console.log(prArr);
    }
    


    for (var c in prArr){
        for (var carrier in data) {
            for (var i in data[carrier]) {
                if (data[carrier][i].price == prArr[c].price && carrier == prArr[c].carrier) {
                    console.log(data[carrier][i]);
                    showCarrier(data[carrier][i])

                }
                
            }  
        }
    }

    
}

function transformDateToString(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000)
    const options = { month: 'long', day: 'numeric' };
    return date.toLocaleDateString(undefined, options);
}

function transformData({name, shippingDate, receivingDate, price}) {
    const logoClassName = `carrier-logo-${name.toLowerCase()}`
    const fromText = shippingDate//transformDateToString(shippingDate)
    const toText = receivingDate//transformDateToString(receivingDate)
    const priceText = `${price}₽`

    return { logoClassName, fromText, toText, priceText }
}

function showCarrier({name, shippingDate, receivingDate, price, tariffId}) {
    console.log('showCarrier - ' + name);
    
    const container = d.createElement('div')
    container.setAttribute('class', 'carrier')
    
    const { logoClassName, fromText, toText, priceText } = transformData({ name, shippingDate, receivingDate, price })

    const nameElement  = d.createElement('div')
    nameElement.classList.add('carrier-logo', logoClassName)

    const shippingDateElement  = d.createElement('div')
    shippingDateElement.setAttribute('class', 'carrier-shipping-date')
    shippingDateElement.textContent = fromText

    const receivingDateElement  = d.createElement('div')
    receivingDateElement.setAttribute('class', 'carrier-receiving-date')
    receivingDateElement.textContent = toText

    const priceElement  = d.createElement('div')
    priceElement.setAttribute('class', 'carrier-price')
    priceElement.textContent = priceText

    const orderButton = d.createElement('button')
    orderButton.setAttribute('class', 'btn btn-default')
    orderButton.textContent = 'Заказать'
    if (name) {
        orderButton.id = name + '-OrderBtn'                
    }

    container.appendChild(nameElement)
    container.appendChild(shippingDateElement)
    container.appendChild(receivingDateElement)
    container.appendChild(priceElement)
    container.appendChild(orderButton)

    const shippingOffers = d.getElementById('shipping-offers')
    //shippingOffers.innerHTML = ''
    shippingOffers.appendChild(container)
    shippingOffers.classList.add('shipping-offers-active')

    orderButton.onclick = function () {
        var cs = this.id.split('-')[0]
        respGlob[this.id.split('-')[0]].func(respGlob[this.id.split('-')[0]].data)
    }
}

$(document).ready(function () {
    var today = new Date();
    var nextDate = new Date(today);
    nextDate.setDate(today.getDate() + 1);
    // d.getElementById('dateExecute').value = nextDate.toISOString().slice(0, 10);
    $("#dateExecute").datepicker({
        format: 'dd.mm.yyyy',
        onRender: function(date) {
            return date.valueOf() < today ? 'disabled' : '';
        }
    });
    $("#dateExecute").datepicker('setValue', nextDate);
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
    $("#close-dpd-order").click(function () {
        $("#dpd-order").fadeOut('fast', function () { $("#calc").fadeIn('fast'); });
    });
    
    $("#dpd-send-order").click(function () {
        console.log("#dpd-send-order");
        d.getElementById('dpd-send-city').innerText = $('#dpd-send-city').text();
        d.getElementById('dpd-recieve-city').innerText = $('#city2').val();
        console.log(); deliveryDataFrom = 'door';
        var fr = deliveryDataFrom == 'door' ? 'T':'Д'
        var to = deliveryDataTo == 'door' ? 'T':'Д'

        var ordProp = {
            'senderAddress' : {
                'name' : $('#dpd-sender-name').val(),
                'terminalCode' : '032L',
                'countryName' : $('#dpd-send-city').text().split(',')[2].replace(' ',''),
                'city' : $('#dpd-send-city').text().split(',')[0],
                'street' : $('#dpd-send-street').val(),
                'house' : $('#dpd-send-house').val(),
                'contactPhone' : $('#dpd-send-phone').val(),
                'contactFio' : $('#dpd-sender-name').val()
            },
             'receiverAddress' : {
                'name' : $('#dpd-reciever-name').val(),
                'terminalCode' : '032L',
                'countryName' : $('#dpd-recieve-city').text().split(',')[2].replace(' ',''),
                'city' : $('#dpd-recieve-city').text().split(',')[0],
                'street' : $('#dpd-reciever-street').val(),
                'house' : $('#dpd-reciever-house').val(),
                'contactPhone' : $('#dpd-reciever-phone').val(),
                'contactFio' : $('#dpd-reciever-name').val()
        
            },
            'order' : {
                'orderNumberInternal' : '123456',
                'serviceCode' : respGlob.dpd.serviceCode,
                'serviceVariant' : fr + to,
                'cargoNumPack' : 1,
                'cargoWeight' : $('#weight').val(),
                'cargoRegistered' : false,
                'cargoCategory' : 'Одежда',
                // 'receiverAddress' : receiverAddress,
        
            }
        }

        // 'height': $('#height').val(),
        // 'width': $('#width').val(),
        // 'weight': $('#weight').val(),
        // 'length': $('#length').val()
        console.log(ordProp);

        
    });
    $("#calcBtn").click(function () {
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
                for (var i in data) {
                    for (var j in respGlob){
                        if (i == j){
                            respGlob[j].data = data[j];
                        }
                    }

                }
                console.log(respGlob);

                
                $('#loader').hide();
                console.log(data);
                showResults(data)
                $('#output').show('fast');
            },
            error: function () {
                $('#loader').hide();
                showResults()
                $('#output').show('fast');
            },
        });
    });
    

  
});
