%global pkg_name ant-contrib
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global beta_number b3

Summary:        Collection of tasks for Ant
Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0
Release:        0.23.%{beta_number}.14%{?dist}
License:        ASL 2.0 and ASL 1.1
URL:            http://ant-contrib.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/ant-contrib/ant-contrib/1.0b3/ant-contrib-1.0b3-src.tar.bz2
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{pkg_name}/%{pkg_name}/1.0b3/%{pkg_name}-1.0b3.pom
# ASL 2.0 Licence text
# Upstream bug at https://sourceforge.net/tracker/?func=detail&aid=3590371&group_id=36177&atid=416920
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
Patch0:         local-ivy.patch
Patch2:         %{pkg_name}-antservertest.patch
Patch3:         %{pkg_name}-pom.patch
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}junit >= 3.8.0
BuildRequires:  %{?scl_prefix_java_common}ant-junit >= 1.6.2
BuildRequires:  %{?scl_prefix_java_common}xerces-j2
BuildRequires:  %{?scl_prefix_java_common}bcel >= 5.0
BuildRequires:  maven30-apache-ivy
Requires:       %{?scl_prefix_java_common}junit >= 3.8.0
Requires:       %{?scl_prefix_java_common}ant >= 1.6.2
Requires:       %{?scl_prefix_java_common}xerces-j2
BuildArch:      noarch

%description
The Ant-Contrib project is a collection of tasks
(and at one point maybe types and other tools)
for Apache Ant.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Api documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%patch0 -b .sav
%patch2

cp %{SOURCE1} %{pkg_name}-1.0b3.pom
%patch3 -p1

cp %{SOURCE2} LICENSE-2.0.txt

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i "s|xercesImpl|xerces-j2|g" ivy.xml
# needs porting to latest ivy
rm -fr src/java/net/sf/antcontrib/net/URLImportTask.java
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
ant dist
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
# jars
install -Dpm 644 target/%{pkg_name}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{pkg_name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d
echo "ant/ant-contrib" > $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d/ant-contrib

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{pkg_name}-1.0b3.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.ant-%{pkg_name}.pom

%add_maven_depmap JPP.ant-%{pkg_name}.pom ant/%{pkg_name}.jar
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/ant
%{_sysconfdir_java_common}/ant.d/ant-contrib
%doc target/docs/LICENSE.txt LICENSE-2.0.txt
%doc target/docs/manual/tasks/*

%files javadoc
%doc target/docs/LICENSE.txt LICENSE-2.0.txt
%doc %{_javadocdir}/%{name}

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0-0.23.b3.14
- maven33 rebuild

* Thu Jan 15 2015 Michal Srb <msrb@redhat.com> - 1.0-0.23.b3.13
- Fix directory ownership

* Thu Jan 15 2015 Michael Simacek <msimacek@redhat.com> - 1.0-0.23.b3.12
- Install ant.d files into rh-java-common's ant.d

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.0-0.23.b3.11
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.0-0.23.b3.10
- Fix BR/R

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.0-0.23.b3.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.0-0.23.b3.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.4
- Remove requires on java

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.3
- SCL-ize requires and build-requires
- Fix Ivy local repo location

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.23.b3.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0-0.23.b3
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.22.b3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.21.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.20.b3
- Added ASL 1.1 licence to the licence field

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.19.b3
- Added LICENSE to javadoc (#879349)
- Added ASL 2.0 licence text (#879354)
- Added requires on jpackage-utils in javadoc (#879356)

* Tue Nov 13 2012 Tomas Radej <tradej@redhat.com> - 1.0-0.18.b3
- Used correct upstream pom + patched it

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.17.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.16.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.15.b3
- Update to beta 3.

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.14.b2
- Fix pom installed name.

* Fri Nov 25 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.13.b2
- Adapt to current guidelines.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.12.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.11.b2
- Add maven pom and depmap.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.10.b2
- Install ant contrib in ant.d.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.9.b2
- Drop gcj_support.
- Install as proper ant plugin.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-0.6.b2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-0.5.b2
- Autorebuild for GCC 4.3

* Sun Aug 03 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.4.b2
- Added dist tag to release.

* Sat Aug 02 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.3.b2
- Removed unneccessary 0 epoch from required packages.
- Fixed dependance on specifically version 3.8.1 of junit.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.2.b2
- Removed Class-Path from ant-contrib.jar file.
- Renamed patches.

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-0.1.b2
- Fixed release number to reflect beta status
- Removed Distribution and Vendor tags
- Fixed duplication in postun section
- Removed patch3, and used sed to fix line-endings instead

* Tue Jun 27 2006 Igor Foox <ifoox@redhat.com> - 1.0-1.b2
- Changed release-version to comply with FE standards
- Consolidated into -manual into main package
- Removed ghosting of the manual symlink
- Removed Epoch
- Run dos2unix over some manual files that have windows line endings
- Changed group for docs to Documentation
- Remove unused Source1
- Set Source0 to valid URL instead of just a file name
- Fix indentation
- Remove {push,pop}d and -c from %%setup
- Changed %%defattr in the %%files section to standard (-,root,root,-)

* Thu Jun 1 2006 Igor Foox <ifoox@redhat.com> - 0:1.0b2-1jpp_1fc
- Update to version 1.0b2
- Added native compilation
- Changed BuildRoot to what Extras expects

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-4jpp
- Upgrade to ant-1.6.2
- BuildReq/Req ant = 0:1.6.2
- Relax some other requirements

* Thu Jun 03 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.6-3jpp
- Fix missing buildrequires

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.6-2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.6-1jpp
- First JPackage release
