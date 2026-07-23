import { Switch, Route } from 'wouter'

import Chat from './pages/Chat'

import './app.css'

function App() {
	return (
		<>
			<Switch>
				<Route path='/chat' component={Chat} />
			</Switch>
		</>
	)
}

export default App
