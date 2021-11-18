Name:           kernel-srpm-macros
Version:        1.0
Release:        12%{?dist}
Summary:        RPM macros that list arches the full kernel is built on
# This package only exist in Fedora repositories
# The license is the standard (MIT) specified in
# Fedora Project Contribution Agreement
# and as URL we provide dist-git URL
License:        MIT
URL:            https://src.fedoraproject.org/rpms/kernel-srpm-macros
BuildArch:      noarch
# We are now the ones shipping kmod.attr
Conflicts:      redhat-rpm-config < 205
# macros.kmp, kmodtool and rpmsort were moved from kernel-rpm-macros
# to kernel-srpm-macros in 1.0-9/185-9
Conflicts:      kernel-rpm-macros < 185-12

# Macros
Source0:        macros.kernel-srpm
Source1:        macros.kmp

# Dependency generator scripts
Source100:      find-provides.ksyms
Source101:      find-requires.ksyms
Source102:      firmware.prov
Source103:      modalias.prov
Source104:      provided_ksyms.attr
Source105:      required_ksyms.attr
Source106:      modalias.attr

# Dependency generators & their rules
Source200:      kmod.attr

# Misc helper scripts
Source300:      kmodtool
Source301:      rpmsort
Source302:      symset-table

# kabi provides generator
Source400: kabi.attr
Source401: kabi.sh

# BRPs
Source500: brp-kmod-set-exec-bit
Source501: brp-kmod-restore-perms

%global rrcdir /usr/lib/rpm/redhat


%description
This packages contains the rpm macro that list what arches
the full kernel is built on.
The variable to use is kernel_arches.

%package -n kernel-rpm-macros
Version: 185
Release: %{release}
Summary: Macros and scripts for building kernel module packages
Requires: redhat-rpm-config >= 13

# for brp-kmod-set-exec-bit
Requires: %{_bindir}/find

%description -n kernel-rpm-macros
Macros and scripts for building kernel module packages.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .


%build
# nothing to do


%install
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d
install -p -m 0644 -t %{buildroot}/%{_rpmconfigdir}/macros.d macros.kernel-srpm
%if 0%{?rhel} >= 8
  sed -i 's/^%%kernel_arches.*/%%kernel_arches x86_64 s390x ppc64le aarch64/' \
    %{buildroot}/%{_rpmconfigdir}/macros.d/macros.kernel-srpm
%endif

mkdir -p %{buildroot}%{rrcdir}/find-provides.d
mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 755 -t %{buildroot}%{rrcdir} kmodtool rpmsort symset-table
install -p -m 755 -t %{buildroot}%{rrcdir} find-provides.ksyms find-requires.ksyms
install -p -m 755 -t %{buildroot}%{rrcdir}/find-provides.d firmware.prov modalias.prov
install -p -m 755 -t %{buildroot}%{rrcdir} brp-kmod-restore-perms brp-kmod-set-exec-bit
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.kmp
install -p -m 644 -t %{buildroot}%{_fileattrsdir} kmod.attr

install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" kabi.attr
install -p -m 755 -t "%{buildroot}%{_rpmconfigdir}" kabi.sh

install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" provided_ksyms.attr required_ksyms.attr
install -p -m 644 -t "%{buildroot}%{_fileattrsdir}" modalias.attr

%files
%{_rpmconfigdir}/macros.d/macros.kernel-srpm
%{_fileattrsdir}/kmod.attr

%files -n kernel-rpm-macros
%{_rpmconfigdir}/macros.d/macros.kmp
%{_rpmconfigdir}/kabi.sh
%{_fileattrsdir}/kabi.attr
%{_fileattrsdir}/modalias.attr
%{_fileattrsdir}/provided_ksyms.attr
%{_fileattrsdir}/required_ksyms.attr
%dir %{rrcdir}/find-provides.d
%{rrcdir}/brp-kmod-restore-perms
%{rrcdir}/brp-kmod-set-exec-bit
%{rrcdir}/symset-table
%{rrcdir}/find-provides.ksyms
%{rrcdir}/find-requires.ksyms
%{rrcdir}/find-provides.d/firmware.prov
%{rrcdir}/find-provides.d/modalias.prov
%{rrcdir}/kmodtool
%{rrcdir}/rpmsort

%changelog
* Thu Nov 18 2021 Miro Hrončok <mhroncok@redhat.com> - 1.0-12
- Correct conflicts to redhat-rpm-macros < 205
- Move Perl scripts back to kernel-rpm-macros to avoid Perl in the default buildroot

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-11
- Add conflicts of redhat-rpm-macros < 204 as macros.kmp, kmodtool,
  and rpmsort were moved from the latter to the former.
- Remove RHEL-specific kABI bits from find-requires.ksyms and macros.kmp.

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-10
- Add conflicts of kernel-srpm-macros with kernel-rpm-macros < 185-9
  as macros.kmp, kmodtool, and rpmsort were moved from the latter
  to the former.

* Thu Nov 18 2021 Eugene Syromiatnikov <esyr@redhat.com> - 1.0-9
- Update scripts with RHEL-specific changes.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Michal Domonkos <mdomonko@redhat.com> - 1.0-5
- Adopt kernel-rpm-macros & kmod.attr subpackage from redhat-rpm-config

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.0-3
- Escape percent for %%kernel_arches macro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Troy Dawson <tdawson@redhat.com> - 1.0-1
- Initial build

