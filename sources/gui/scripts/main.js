function startSimulation(config)
{
	eel.startSimulationPy(config)
}

function createJSONFromConfig()
{
	json_conf = {
		'imNum' : document.getElementById('imNum').value,
		'host' : document.getElementById('host').value,
		'port' : document.getElementById('port').value,
		'width' : document.getElementById('width').value,
		'height' : document.getElementById('height').value,
		'fov' : document.getElementById('fov').value,
		'day' : document.getElementById('day').value,
		'night' : document.getElementById('night').value,
		'traffic' : document.getElementById('traffic').value
	}

	return json_conf
}

function mountButton()
{
	btn = document.getElementById('generate-button')

	btn.addEventListener('click', () => {
		startSimulation(createJSONFromConfig())
	})
}