#!/bin/sh
# NIC_DOCTOR_RELEASE v1.0.7
# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
# Generated from src/ by build.sh.
# Requires Python 3.9+.
# The complete license terms are included below.
: <<'NIC_DOCTOR_LICENSE'
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
NIC_DOCTOR_LICENSE
set -eu
if ! command -v python3 >/dev/null 2>&1; then
  echo 'nic-doctor: Python 3.9+ is required' >&2
  exit 1
fi
exec python3 - "$0" "$@" <<'NIC_DOCTOR_BOOTSTRAP'
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import secrets
import sys

if sys.version_info < (3, 9):
    raise SystemExit('nic-doctor: Python 3.9+ is required')
script_path = Path(sys.argv[1]).absolute()
args = sys.argv[2:]
blob = script_path.read_bytes()
marker = b'\n__NIC_DOCTOR_EMBEDDED_PAYLOAD__\n'
if blob.count(marker) != 1:
    raise SystemExit('nic-doctor: embedded payload missing or damaged')
encoded = b''.join(blob.split(marker, 1)[1].split())
try:
    payload = gzip.decompress(base64.b64decode(encoded, validate=True))
except (OSError, ValueError) as exc:
    raise SystemExit('nic-doctor: embedded payload damaged: ' + str(exc))
if hashlib.sha256(payload).hexdigest() != 'c6f38fe3872f6e1fa43bd331ed912368105b62c07c92313f331e130d3e122fd1':
    raise SystemExit('nic-doctor: embedded payload hash mismatch')
compile(payload, str(script_path), 'exec')

if args and args[0] == 'install':
    if sys.platform != 'linux':
        raise SystemExit('nic-doctor: Linux required')
    if os.geteuid() != 0:
        raise SystemExit('nic-doctor: root required (sudo ./nic-doctor.sh install)')
    if len(args) == 1:
        prefix = Path('/usr/local')
    elif len(args) == 3 and args[1] == '--prefix':
        prefix = Path(args[2])
    else:
        raise SystemExit('Usage: sudo ./nic-doctor.sh install [--prefix /usr/local]')
    if not prefix.is_absolute() or '..' in prefix.parts or prefix.is_symlink():
        raise SystemExit('nic-doctor: invalid installation prefix')
    executable = prefix/'bin/nic-doctor'
    manifest = prefix/'lib/nic-doctor/install.json'
    if executable.is_symlink() or manifest.is_symlink():
        raise SystemExit('nic-doctor: refusing symlink installation path')
    if executable.exists():
        if not manifest.is_file():
            raise SystemExit('nic-doctor: unrecognized existing executable; refusing overwrite')
        try:
            old = json.loads(manifest.read_text())
            existing_hash = hashlib.sha256(executable.read_bytes()).hexdigest()
        except (OSError, ValueError) as exc:
            raise SystemExit('nic-doctor: unreadable installation state: '+str(exc))
        if (old.get('marker') != 'NIC_DOCTOR_RELEASE' or
            old.get('binary') != str(executable) or old.get('sha256') != existing_hash):
            raise SystemExit('nic-doctor: existing executable modified; refusing overwrite')
    elif manifest.exists():
        raise SystemExit('nic-doctor: orphaned installation manifest; refusing overwrite')
    contents = blob
    exe_hash = hashlib.sha256(contents).hexdigest()
    meta = {'marker': 'NIC_DOCTOR_RELEASE', 'version': '1.0.7',
            'binary': str(executable), 'sha256': exe_hash}
    for target, data, mode in ((executable, contents, 0o755),
                               (manifest, (json.dumps(meta, indent=2)+'\n').encode(), 0o644)):
        target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        temp = target.with_name('.'+target.name+'.'+secrets.token_hex(8)+'.tmp')
        fd = os.open(temp, os.O_CREAT|os.O_EXCL|os.O_WRONLY, mode)
        try:
            with os.fdopen(fd, 'wb') as out:
                out.write(data)
                out.flush()
                os.fsync(out.fileno())
            os.chmod(temp, mode)
            os.replace(temp, target)
        finally:
            if temp.exists():
                temp.unlink()
    print('Installed '+str(executable)+' (v1.0.7)')
    print('Run: nic-doctor topology')
    print('Remove: sudo nic-doctor remove')
    raise SystemExit(0)

sys.argv = [str(script_path)] + args
scope = {'__name__': '__main__', '__file__': str(script_path), '__package__': None}
exec(compile(payload, str(script_path), 'exec'), scope)
NIC_DOCTOR_BOOTSTRAP
exit $?
__NIC_DOCTOR_EMBEDDED_PAYLOAD__
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
Aycp6gAA
