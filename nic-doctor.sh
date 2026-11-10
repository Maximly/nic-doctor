#!/bin/sh
# NIC_DOCTOR_RELEASE v1.1.1
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
if hashlib.sha256(payload).hexdigest() != 'd2b1b8d289dd39bc51a857560742f7db556503f90721bd259f9f5a7658c25d79':
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
    meta = {'marker': 'NIC_DOCTOR_RELEASE', 'version': '1.1.1',
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
    print('Installed '+str(executable)+' (v1.1.1)')
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
