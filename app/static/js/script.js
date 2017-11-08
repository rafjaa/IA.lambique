
$(document).ready(function(){
	var count=0; 

	 $('.modal').modal();

	 function processa_dados_grafico(dict){

		// Create items array
		var items = Object.keys(dict).map(function(key) {
		    return [key, dict[key]];
		});

		// Sort the array based on the second element
		items.sort(function(first, second) {
		    return second[1] - first[1];
		});

		labels = []
		values = []
		for (var i = 0; i < items.length; i++){
			labels.push(items[i][0])
			values.push(items[i][1])
		}
		return [labels, values]

	}

	function getRandomColorEachEmployee(count) {
        var data =[];
        for (var i = 0; i < count; i++) {
            data.push(getRandomColor());
        }
        return data;
    }

	function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16	)] + 0.2;

        }
        return color;
    }

	// Carrega informações armazenadas
	function obtem_modelo_carregado(){
		$.get('/info', function(data){
			$('#modelo_carregado').html(
				'<li>Nome do arquivo: <strong>' + data.filename + '</strong></li>Eficiência: <strong>' + data.pontuacao.toFixed(3)*100 + ' 	%</strong></li>')

				// Gráfico
				data = processa_dados_grafico(data.fscore)
				var ctx = $('#grafico');

				var grafico = new Chart(ctx, {
					type: 'horizontalBar',
					data: {
						labels: data[0],
						datasets: [{
							label:"Pontuação",
							data: data[1],
							backgroundColor: 'rgba(255, 0, 0, 0.4)',//getRandomColorEachEmployee(data[0].length),
							

						}]
					},
					options:{
						title: {
							display: true,
							text: '',//'Importância dos parâmetros',
							fontSize: 30
						},
						legend: {
							display: false
						},

						scales: {
							xAxes: [{
								ticks: {
									display: false,

								}
							}]
						},
					}
				});

		}, 'json')
	}
	obtem_modelo_carregado();
	
	// Envia um arquivo via ajax
	var uploadObj = $("#fileuploader").uploadFile({
		url: "/dados",
		fileName:"file",
		maxFileCount: 1,
		onSuccess: function(files, data, xhr, pd){
			result = JSON.parse(data)
			console.log('Resultado' + data);

			if (result.status == 1)
				$('#erro').text('Ocorreu um erro no processamento verifique seus dados de entrada!')

			obtem_modelo_carregado();			

			// Evita cache da imagem
			img = $("#features_importance")
			img.attr('src', img.attr('src') + new Date().getTime());
		},
		onError: function(files,status,errMsg,pd){
		    errMsg: alert('Erro!')
		},
		allowedTypes: 'csv',
		showDelete: true,
		showStatusAfterSuccess: true,
		uploadStr: 'Enviar arquivo',
		autoSubmit: false,
		extErrorStr: 'Selecione um arquivo válido! ',
		
		afterUploadAll: function(obj){
			uploadObj.reset();
		},
		onSelect:function(files){
	       // Limpa caixa de erro
	       $('#erro').text('');
	       
	       $('#modal1').modal('open');
	       
	       $('#enviar_sim').click(function(){
	       		uploadObj.startUpload();
	       });

	       $('#enviar_nao').click(function(){
	       		uploadObj.reset();
	       });

	   	},
	});

	// Carrega formulário de simulação
	$('#card_simulacao').click(function(){
			
		$.get('/simulacao', function(data){
			
			// Oculta barra progresso
  			$('.progress').hide();
			
			$.get('/static/js/template.html?v=' + Math.random(), function(template){
				
				// Oculta barra progresso
  				$('.progress').hide();

				features = data['features'];
				
				for (i = 0; i < features.length; i++){
					features[i]['index'] = i;
				}

				$('#features').empty();

				// Preenche features
				$.tmpl(template, features).appendTo('#features')			
			});
			
		}, 'json');
	});

	// Quando um range mudar calcula nota para features
	$('#form_simulacao').change(function(e){

		// Previne comportamento default do form.
		e.preventDefault();

		// Dados do formulário
		var data = $(this).serialize()

		$.post("/simulacao", data, function(data) {
  
  			$('#nota').text(data['y_label'] + ': ' + data['nota']);
  			Materialize.toast(data['y_label'] + ': ' + data.nota, 4000, 'rounded')

		},'json').fail(function(){
			console.log('Erro');
		})
	})

	// Exibe e esconde botão voltar ao topo
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('a[href="#top"]').fadeIn();
        } else {
            $('a[href="#top"]').fadeOut();
        }
    });
});

