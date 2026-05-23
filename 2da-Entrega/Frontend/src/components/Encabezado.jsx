import { NavLink } from 'react-router-dom';

export default function Encabezado() {
    return (
        <header className="bg-dark text-white py-3 mb-4">
            <div className="container py-5 h-100 position-relative">
                <div className="usuario-pill">
                    <i className="bi bi-person-circle"></i>
                    <span>TP Simulacion G5</span>
                </div>
                <nav className="mt-3">
                  <ul
                      className="nav nav-pills nav-fill gap-2 p-1 small bg-primary rounded-5 shadow-sm justify-content-center"
                      id="pillNav"
                  >
                      <li className="nav-item">
                          <NavLink
                              to="/simulacion"
                              className="nav-link rounded-5"
                              activeclassname="active"
                          >
                              Ir a Simular 
                          </NavLink>
                        </li>
                     
                  </ul>
                </nav>
            </div>
        </header>
    );
}
