
# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%global with_python3 0


%global library kubernetes

Name:       python-%{library}
Version:    11.0.0
Release:    1%{?dist}
Summary:    Python client for the kubernetes API.
License:    ASL 2.0
URL:        https://pypi.python.org/pypi/kubernetes

Source0:    https://github.com/kubernetes-incubator/client-python/archive/v%{version}.tar.gz
Source1:    https://github.com/kubernetes-client/python-base/archive/d30f1e6fd4e2725aae04fa2f4982a4cfec7c682b.tar.gz 
BuildArch:  noarch

%package -n python2-%{library}
Summary:    Kubernetes Python Client
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python-py
# BuildRequires:  python-mock
BuildRequires:  python-certifi
BuildRequires:  python-six
BuildRequires:  python-dateutil
BuildRequires:  python-setuptools
BuildRequires:  python-urllib3
BuildRequires:  PyYAML
BuildRequires:  python-google-auth
BuildRequires:  python-ipaddress

Requires:  python-certifi
Requires:  python-six
Requires:  python-dateutil
Requires:  python-setuptools
Requires:  python-urllib3
Requires:  PyYAML
Requires:  python-google-auth
Requires:  python-ipaddress
Requires:  python-websocket-client
Requires:  python-requests
Requires:  python-requests-oauthlib

%description -n python2-%{library}
Python client for the kubernetes API.


%package -n python2-%{library}-tests
Summary:    Tests python-kubernetes library

Requires:  python-nose
Requires:  python-py
Requires:  python-mock
Requires:  python2-%{library} = %{version}-%{release}


%description -n python2-%{library}-tests
Tests python-kubernetes library

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    Kubernetes Python Client
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
# BuildRequires:  python3-nose
# BuildRequires:  python3-py
# BuildRequires:  python3-mock
BuildRequires:  python3-certifi
BuildRequires:  python3-six
BuildRequires:  python3-dateutil
BuildRequires:  python3-setuptools 
BuildRequires:  python3-urllib3
BuildRequires:  python3-PyYAML
BuildRequires:  python3-google-auth
BuildRequires:  python3-websocket-client

Requires:  python3-certifi
Requires:  python3-six
Requires:  python3-dateutil
Requires:  python3-setuptools 
Requires:  python3-urllib3
Requires:  python3-PyYAML
Requires:  python3-google-auth
Requires:  python3-websocket-client

%description -n python3-%{library}
Python client for the kubernetes API.


%package -n python3-%{library}-tests
Summary:    Tests python-kubernetes library

Requires:  python3-nose
Requires:  python3-py
Requires:  python3-mock
Requires:  python3-%{library} = %{version}-%{release}


%description -n python3-%{library}-tests
Tests python-kubernetes library


%endif # with_python3


%description
Python client for the kubernetes API.

%prep
%autosetup -n python-%{version} -S git

pushd kubernetes
rm -rf base
tar zxvf %{SOURCE1}

mv python-base-d30f1e6fd4e2725aae04fa2f4982a4cfec7c682b base
popd

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Currently recommonmark requires an old version of commonmark,
# commonmark (<=0.5.4) wich doesn't exist in fedora rawhide so
# we disable docs generation until recommonmark is fixed to be
# compatible with recent version.
# generate html docs
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
cp -pr kubernetes/test %{buildroot}%{python2_sitelib}/%{library}/
cp -pr kubernetes/e2e_test %{buildroot}%{python2_sitelib}/%{library}/
%if 0%{?with_python3}
%py3_install
cp -pr kubernetes/test %{buildroot}%{python3_sitelib}/%{library}/
cp -pr kubernetes/e2e_test %{buildroot}%{python3_sitelib}/%{library}/
%endif

%check

%files -n python2-%{library}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{library}
%{python2_sitelib}/%{library}-*.egg-info
%exclude %{python2_sitelib}/%{library}/test
%exclude %{python2_sitelib}/%{library}/e2e_test

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{library}/test
%{python2_sitelib}/%{library}/e2e_test

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{library}
%{python3_sitelib}/%{library}-*.egg-info
%exclude %{python3_sitelib}/%{library}/test
%exclude %{python3_sitelib}/%{library}/e2e_test

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{library}/test
%{python3_sitelib}/%{library}/e2e_test
%endif # with_python3

%changelog
* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Feb 28 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.3.0b3
- Remove BRs for documentation building as it's not creating html docs.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.2.0b3
- Fixed %files section of python3-kubernetes-tests to contain python3 tests.

* Mon Feb 27 2017 Alfredo Moralejo <amoralej@redhat.com> 1.0.0-0.1.0b3
- Initial spec for release 1.0.0b3
