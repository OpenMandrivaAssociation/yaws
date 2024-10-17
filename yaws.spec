Summary:	A high performance HTTP 1.1 webserver
Name:		yaws
Version:	1.87
Release:	2
License:	BSD
Group:		System/Servers
Url:		https://yaws.hyber.org/
Source0:	http://yaws.hyber.org/download/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-1.87-makefile.patch
Patch1:		%{name}-1.77-www.patch
BuildRequires:	erlang-compiler
BuildRequires:	erlang-devel
BuildRequires:	erlang-mnesia
BuildRequires:	erlang-xmerl
BuildRequires:	erlang-dialyzer
BuildRequires:	pam-devel
Requires:	erlang-mnesia
Requires:	erlang-xmerl
Requires:	erlang-crypto
Requires:	erlang-compiler
Requires:	erlang-dialyzer
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Yaws is a HTTP high perfomance 1.1 webserver particularly 
well suited for dynamic-content webapplications. Two separate 
modes of operations are supported.

* Standalone mode where Yaws runs as a regular webserver daemon. 
  This is the default mode.
* Embedded mode where Yaws runs as an embedded webserver in another 
  erlang application

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# (tpg) fix pc file
sed -i -e 's@$(PREFIX)/lib/pkgconfig@$(LIBDIR)/pkgconfig@g' Makefile
sed -i -e 's@/lib@/%{_lib}@g' *.pc.in

%configure2_5x \
	--with-defaultcharset=UTF-8 \
	--sysconfdir=%{_sysconfdir}/%{name}

# (tpg) limit threads to 4, so it can build on x86_64
%make BINDIR=%{_bindir} LIBDIR=%{_libdir} -j4

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std BINDIR=%{_bindir} LIBDIR=%{_libdir}

mkdir -p %{buildroot}%{_initrddir}
mv -f %{buildroot}%{_sysconfdir}/%{name}/init.d/%{name} %{buildroot}%{_initrddir}/%{name}

# (tpg) remove autogenerated config
rm -rf %{buildroot}%{_sysconfdir}/%{name}.conf

rm -rf %{buildroot}%{_sysconfdir}/%{name}/init.d

# (tpg) install custom config
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%pre
%_pre_useradd %{name} /var/yaws/www /bin/sh

%post
%_post_service %{name}

%postun
%_postun_userdel %{name}

%preun
%_preun_service %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog 
%dir %{_sysconfdir}/%{name}
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_initrddir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/%{name}*.5.*
%{_var}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%exclude %{_docdir}/%{name}-%{version}


%changelog
* Sun Feb 28 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.87-1mdv2010.1
+ Revision: 512744
- rediff patch 0
- update to new version 1.87
- update to new version 1.85
- disable patch 0

* Sun Aug 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1.84-1mdv2010.0
+ Revision: 412557
- update to new version 1.84

* Wed Jun 17 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.82-3mdv2010.0
+ Revision: 386827
- rebuild for new erlang

* Mon Jun 15 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.82-2mdv2010.0
+ Revision: 386165
- fix pkgconfig file
- make it build on x86_64 by limiting max jobs to 4 while compiling

  + Frederik Himpe <fhimpe@mandriva.org>
    - Re-add makefile patch: it's still needed
    - Update to new version 1.82
    - Remove makefile patch: not needed anymore

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.77-5mdv2009.1
+ Revision: 308021
- Patch1: fix system path
- config file looks nicer now

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.77-4mdv2009.1
+ Revision: 307859
- fix config file
- add missing requires on erlang-cryptop, erlang-compiler and erlang-dialyzer
- move config files to /etc/yaws
- add scriplets

* Fri Aug 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.77-3mdv2009.0
+ Revision: 277145
- rebuild
- Patch0: fix install on x86_64
- add missing buildrequires
- fix rpm group and license
- import yaws


