import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
	return (
		<>
			<Nav>
				<NavMenu>
					<NavLink to="/" activeStyle>
						HOME
					</NavLink>
					<NavLink to="/all-basic" activeStyle>
						ALL BASIC
					</NavLink>
					<NavLink to="/search-basic" activeStyle>
						SEARCH BASIC
					</NavLink>
				</NavMenu>
			</Nav>
		</>
	);
};

export default Navbar;
