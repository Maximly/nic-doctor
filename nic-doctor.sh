#!/bin/sh
# NIC_DOCTOR_RELEASE v1.1.0
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
if hashlib.sha256(payload).hexdigest() != 'ebb0071a6dda971608508902061230a52353335c88d6c433deba2170c804b711':
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
    meta = {'marker': 'NIC_DOCTOR_RELEASE', 'version': '1.1.0',
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
    print('Installed '+str(executable)+' (v1.1.0)')
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
