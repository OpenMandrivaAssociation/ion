%define name    ion
%define version 20040729
%define release 5
%define prefix  /usr

%define	ionetc  %_sysconfdir/X11/%name

Summary:	Tiling window manager with keyboard-oriented interface
Name:		%name
Version:	%version
Release:	%mkrel %release
Group:		Graphical desktop/Other
License:	Artistic
URL: 		http://modeemi.cs.tut.fi/~tuomov/ion/
Source0: 	http://modeemi.cs.tut.fi/~tuomov/ion/dl/%name-2-%version.tar.bz2
Source1:	http://modeemi.cs.tut.fi/~tuomov/ion/dl/%name-doc-2-%version.tar.bz2
BuildRoot:	%_tmppath/%name-buildroot
BuildRequires:  freetype2-devel libltdl-devel
BuildRequires:  liblua-devel >= 5, lua
BuildRequires:  X11-devel
BuildRequires:  chrpath perl
Requires:	xterm
# for xmessage
Requires:	X11R6-contrib

%description
Ion was written as an experiment on a different kind of window man-
agement model and it tries to address the navigation problem by hav-
ing the screen divided into frames that take up the whole screen and
never overlap.

Read the manpage or go nuts

%prep
%__rm -rf $RPM_BUILD_ROOT
%setup -q -n %name-2-%version

tar xjf %{SOURCE1}

# Fix path-names in the manpage.
%__perl -pi -e "s#ETCDIR#"%ionetc"#g"       man/%name.1.in
%__perl -pi -e "s#.I DOCDIR/##g"            man/%name.1.in
# %__perl -pi -e "s#.I X\(1x\)/#.I X(7x)#g"   man/%name.1.in


%build
./configure --datadir=%{_datadir} --libdir=%{_libdir}
%make

chrpath -d ./pwm/pwm
chrpath -d ./ion/ion


%install
%__rm -rf $RPM_BUILD_ROOT

%__make install	PREFIX=%buildroot%prefix \
		MANDIR=%buildroot%prefix/share/man \
 		DOCS= \
		ETCDIR=%buildroot%ionetc \
                LUA_DIR=%_prefix \
		MODULEDIR=%buildroot%prefix/%_lib/ion \
		SHAREDIR=%buildroot%prefix/share/ion \
		LCDIR=%buildroot%prefix/%_lib/ion/lc \
		BINDIR=%buildroot%prefix/bin \
		EXTRABINDIR=%buildroot%prefix/%_lib/ion \
		DOCDIR=%buildroot%prefix/share/doc

# Like somebody would need to link against ion in the near future.
%__rm %buildroot%prefix/%_lib/%name/*.a

%__mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/wmsession.d
%__cat >    $RPM_BUILD_ROOT%_sysconfdir/X11/wmsession.d/14%name << EOF
NAME=%name
EXEC=%prefix/bin/%name
DESC=%summary
SCRIPT:
exec %prefix/bin/%name
EOF

# Avoid conflict with pwm
mv %buildroot%prefix/bin/pwm %buildroot%prefix/bin/pwm-%name

# # install doc
# cd ion-doc-*
# %__make install PREFIX=%buildroot%prefix
# cd -


%post
%make_session

%postun
%make_session

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)
%prefix/bin/*
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README ion-doc*/ionconf*
# %prefix/man/man1/*
%prefix/share/man/man1/*
%dir %ionetc
%config(noreplace) %ionetc/*
%config(noreplace) %_sysconfdir/X11/wmsession.d/14%name
%defattr(-,root,root,755)
%dir %prefix/%_lib/%name
%prefix/%_lib/%name/*
%dir %prefix/share/%name
%prefix/share/%name/*


