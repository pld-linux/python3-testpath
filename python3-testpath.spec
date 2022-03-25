#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Test utilities for code working with files and commands
Summary(pl.UTF-8):	Narzędzia testowe dla kodu działającego na plikach i poleceniach
Name:		python3-testpath
Version:	0.6.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testpath/
Source0:	https://files.pythonhosted.org/packages/source/t/testpath/testpath-%{version}.tar.gz
# Source0-md5:	9fd4339f76da12d15bc718e4aa2566e9
URL:		https://pypi.org/project/testpath/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Testpath is a collection of utilities for Python code working with
files and commands.

It contains functions to check things on the filesystem, and tools for
mocking system commands and recording calls to those.

%description -l pl.UTF-8
Testpath to zbiór narzędzi dla kodu w Pythonie działającego na plikach
i poleceniach.

Zawiera funkcje do sprawdzania elementów w systemie plików oraz
narzędzia do tworzenia atrap poleceń systemowych i zapisywania ich
wywołań.

%package apidocs
Summary:	API documentation for Python testpath module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona testpath
Group:		Documentation

%description apidocs
API documentation for Python testpath module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona testpath.

%prep
%setup -q -n testpath-%{version}

# setuptools stub
cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

# until we have flit...
# (extracted from pyproject.toml - keep in sync!)
cat >setup.cfg <<'EOF'
[metadata]
name = testpath
version = %{version}
description = Test utilities for code working with files and commands
author = Jupyter Development Team
author_email = jupyter@googlegroups.com
license = BSD
license_file = LICENSE
classifiers =
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 3
    Topic :: Software Development :: Testing
[options]
packages = testpath
python_requires = >=3.5
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/testpath
%{py3_sitescriptdir}/testpath-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
