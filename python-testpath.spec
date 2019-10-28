#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Test utilities for code working with files and commands
Summary(pl.UTF-8):	Narzędzia testowe dla kodu działającego na plikach i poleceniach
Name:		python-testpath
Version:	0.4.2
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testpath/
Source0:	https://files.pythonhosted.org/packages/source/t/testpath/testpath-%{version}.tar.gz
# Source0-md5:	562d0e1b02fc5cbcb8406955bcd7249f
URL:		https://pypi.org/project/testpath/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%if %{with tests}
BuildRequires:	python-pathlib2
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-testpath
Summary:	Test utilities for code working with files and commands
Summary(pl.UTF-8):	Narzędzia testowe dla kodu działającego na plikach i poleceniach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-testpath
Testpath is a collection of utilities for Python code working with
files and commands.

It contains functions to check things on the filesystem, and tools for
mocking system commands and recording calls to those.

%description -n python3-testpath -l pl.UTF-8
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

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/testpath
%{py_sitescriptdir}/testpath-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-testpath
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/testpath
%{py3_sitescriptdir}/testpath-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
