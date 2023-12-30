import "./App.css"
import "primereact/resources/themes/lara-light-cyan/theme.css"

import { store } from "./app/store"
import { NavBar } from "./common/components/NavBar"
import { PrimeReactProvider } from "primereact/api"
import { Provider } from "react-redux"

function App() {
  return (
    <PrimeReactProvider>
      <Provider store={store}>
        <div className="App">
          <NavBar />
        </div>
      </Provider>
    </PrimeReactProvider>
  )
}

export default App
