# EA4 openssl on C8 and beyond

## Target Audiences

1. Maintenance and security teams
2. Training and technical support
3. Managers and other internal key stakeholders
4. Future project/feature owners/maintainers

## Detailed Summary

*   ea-openssl11, was built with the sym-variant flag, where our symbols are OPENSSL\_EA\_1\_1\_1, instead of OPENSSL\_1\_1\_1.
    *   This was done a few years ago, with the intent our library would not interfere with the system openssl library.
    *   Our symbols would only satisfy with our library.
    *   That worked great on C6 and C7.  But on C8 this has become untenable.
        *   On C8
        *   I have to link our executables and dynamic libraries against both our ea-openssl11, and system openssl.
        *   The reason is because:
            *   I would satisfy all of our libraries and executables with ea-openssl11 symbols
            *   But because of the way C8 is designed, I need to bring in other libraries which are built agains system openssl only.
            *   So much confusion because of the doubly linked files.
            *   That is probably unstable as well.
    *   Why did we create ea-openssl11 in the first place?
        *   Back in the C5, C6 days, system openssl was no longer kept up to date on the distro.
        *   We introduced ea-openssl, and kept is secure.
        *   We further added features necessary to cPanel.
        *   At one point, we needed openssl11 for both security and feature set issues.
        *   Well C6 was not going to support openssl11, so we created ea-openssl11.
        *   We then were able to continue.
    *   Our current plan is to build all of our C8 products against system openssl.
        *   This is primarily because ea-openssl11, has the sym variant option.
        *   We have evaluated modifying ea-openssl11 to not use the sym variant, which is discussed later.
        *   We chose the system openssl to simplify the builds/linking steps.
        *   The distro has the incentive to maintain the openssl library and will do so for a long time, perhaps 4 years or longer.
        *   That means our duplicate openssl is just a maintenance burden.
        *   The links will be so much easier.
        *   We do have to change a lot of rpms, but this should be a non breaking set of changes.
        *   At some point we may have to revisit this and create the openssl11 without the sym variant discussed below.
        *   This is **not** a breaking set of changes.
    *   Alternative plan, update ea-openssl11, to not have the sym variant options
        *   This is doable, but we found out something disturbing.
        *   The intent is all of our executables and dynamic libraries would be built against ea-openssl11, and the external libraries we bring in would satisfy their openssl symbols against our library and not the system library.
        *   This simplifies the building and linking significantly.
        *   There are a bunch of gotcha’s.
            *   First and foremost, this is a breaking change.  They will have to update the entire ea stack, and it would make downgrading very difficult at this point.
            *   Second and just as big, vanilla openssl is not sufficient.  Fedora/CentOS/Redhat brought entire features into openssl11, from openssl3.0.
                *   Openssl 3.0 is in alpha state
                *   So they created a series of patches to bring those features into openssl 1.1.
                *   We would have to copy those patches into ours and either maintain them ourselves, or continue to pull them in and perhaps patch the patches.
                *   This makes our openssl 11 maintenance burden very high.
    *   If we go with either option, we have to rebuild the full stack.
        *   Doing ea-openssl11 would be a breaking change
        *   Doing system openssl11 is not a breaking change

## Overall Intent

Find the most sustainable way to do openssl for EA4 on C8 and beyond.

## Maintainability

Included in table below.

## Options/Decisions

**Note**: Options will need `if > 7 else` logic in 13 packages in addition to libcurl and ruby 2.7 that are in play already. Would also mean doing the system libcurl on C8.

<!-- from wiki’s “View Storage Format” -->
<table><colgroup><col /><col /><col /><col /><col /></colgroup>
<tbody>
<tr>
<th>OPTIONS</th>
<th>VALUE</th>
<th>DRAWBACK</th>
<th>MAINTENANCE</th>
<th>DECISION</th></tr>
<tr>
<td>Use System openssl</td>
<td>
<ul>
<li>Fedora/CentOS handles maintenance of the package</li>
<li>Less work for EA/ZC on C8</li></ul>
<p><br /></p></td>
<td>
<ul>
<li>C8 will get old eventually and the package will be on its last leg</li>
<li>We will likely need to build ea-openssl30 by then anyway</li></ul></td>
<td>
<ul>
<li>None</li></ul></td>
<td>
<ul>
<li>At this time, we think this is the way to go</li></ul></td></tr>
<tr>
<td>ea-openssl11 w/ Fedora patchset</td>
<td>
<ul>
<li>Customers get a preview of openssl 3.0 features that are currently in alpha</li></ul></td>
<td>
<ul>
<li>Is it really any newer or providing anything more than system openssl at this point?</li>
<li>Hard to maintain as will need a way to track changes to fedora's patches for upgrades as well</li>
<li>Easy to miss CVEs being fixed in fedora's patchset</li></ul></td>
<td>
<ul>
<li>We will need to keep the version of openssl up to date</li>
<li>We will also need to monitor fedora's patchset for new patches and bug fixes being added to existing patches and update as necessary for those</li></ul></td>
<td>
<ul>
<li>Not doing this as it increasing risk without providing enough value</li></ul></td></tr>
<tr>
<td colspan="1">ea-openssl11 w/out Fedora patchset (what we are currently doing)</td>
<td colspan="1">
<ul>
<li>None, our version of openssl would technically be older than system since system openssl has openssl 3.0 features in it</li></ul></td>
<td colspan="1">
<ul>
<li>Linking is very difficult and time consuming</li>
<li>We end up linked against our openssl and system openssl due to the system packages that we bring in requiring openssl 3.0 features provided by the system</li></ul></td>
<td colspan="1">
<ul>
<li>Untenable</li></ul></td>
<td colspan="1">
<ul>
<li>No, just no</li></ul></td></tr>
<tr>
<td colspan="1">ea-openssl11 w/out Fedora patchset but we build the world to compile against ea-openssl11</td>
<td colspan="1">
<ul>
<li>Everything just links against our openssl</li></ul></td>
<td colspan="1">
<ul>
<li>Increases maintenance burden significantly</li>
<li>We incur risk for CVEs as they come up (we would likely need to have multiple EA maintenance releases per week)</li></ul></td>
<td colspan="1">
<ul>
<li>Untenable</li></ul></td>
<td colspan="1">
<ul>
<li>Do we really want to become cPanel OS?</li></ul></td></tr></tbody></table>

### Conclusion

Go with system openssl on C8 for now. Revisit as needed as time passes and probably do this dance again w/ ea-openssl30.

## Child Documents

None.
