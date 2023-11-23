# Copyright 1999-2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8

if [[ ${PV} == 9999* ]] ; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/csfore/todo.git"
fi

HOMEPAGE="https://github.com/csfore/todo"
DESCRIPTION="Todo program to help enhance your Gentoo workflow"

LICENSE="GPL3"
SLOT="0"
KEYWORDS="~amd64"

src_install() {
	dobin todo
}
