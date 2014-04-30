#!/usr/bin/perl -w
use strict;
use Getopt::Std;

sub maximum(@);
sub readList($\%);
sub pushPair($$);

my $font = 'Times-Roman';
my $fontsize = 12;
my $em = 0.6;  # expected em-to-font-size ratio
my $padding = 5;
my $linepad = 2.5;

my(%opts, %lefts, %tops, %matrix);
getopts('1:2:TSm', \%opts) || exit 2;
@opts{'1','2'} = @opts{'2','1'} if $opts{T};

my($rows, $cols) = (0, 0);
$rows = readList $opts{1}, %lefts if defined $opts{1};
$cols = readList $opts{2}, %tops  if defined $opts{2};

while (<>) {
 chomp;
 s/\s+$//;
 next if /^$/ || /^\s*#/;
 my($left, @top) = split /\t+/;
 if ($opts{m}) { pushPair($left, $_) for @top }
 elsif (@top) { pushPair($left, $top[0]) }
}

if (!$opts{S}) {
 if (!defined $opts{1}) {
  my $i = 0;
  %lefts = map { $_ => $i++ } sort keys %matrix;
  $rows = $i;
 }
 if (!defined $opts{2}) {
  my $i = 0;
  %tops = map { %$_ } values %matrix;
  $tops{$_} = $i++ for sort keys %tops;
  $cols = $i;
 }
}

my $leftlen = maximum(map length, keys %lefts) * $em * $fontsize;
my $toplen  = maximum(map length, keys %tops)  * $em * $fontsize;

my $miny = $rows * $fontsize * 1.2;
my $maxx = $cols * $fontsize * 1.2;

print <<EOT;
%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: -@{[$leftlen+$padding]} -@{[$miny+$padding]} @{[$maxx+$padding]} @{[$toplen+$padding]}
/fontsize $fontsize def
/$font findfont fontsize scalefont setfont
/lineheight fontsize 1.2 mul def
/radius lineheight 3 div def

0.8 0.8 0.8 setrgbcolor
0 2 $cols 1 sub {
 lineheight mul -$miny lineheight $miny $toplen add rectfill
} for

1 1 0.5 setrgbcolor
2 2 $rows {
 % Yes, it starts at 2, so that the positive rectfill height will make it fill
 % row 1.
 lineheight mul neg -$leftlen exch $leftlen $maxx add lineheight rectfill
} for

0 0 0 setrgbcolor
newpath 0   $toplen moveto 0 -$miny lineto stroke
newpath -$leftlen 0 moveto $maxx  0 lineto stroke

/dot {
 0.5 add lineheight mul exch 0.5 add lineheight mul neg radius 0 360 arc fill
} def
EOT

while (my($key, $i) = each %lefts) {
 (my $left = $key) =~ s/([(\\)])/\\$1/g;
 print <<EOT;
($left) dup stringwidth pop neg $linepad sub
$i 1 add lineheight mul neg fontsize 3 div add
moveto
show
EOT
}

while (my($key, $i) = each %tops) {
 (my $top = $key) =~ s/([(\\)])/\\$1/g;
 print <<EOT;
gsave
$i 1 add lineheight mul 0 translate 90 rotate $linepad fontsize 3 div moveto
($top) show
grestore
EOT
}

for (grep { exists $lefts{$_} } keys %matrix) {
 my $rowNo = $lefts{$_};
 print "$rowNo $tops{$_} dot\n"
  for grep { exists $tops{$_} } keys %{$matrix{$_}};
}

print "showpage\n";

sub maximum(@) {
 my $max = shift;
 for (@_) { $max = $_ if $_ > $max }
 return $max;
}

sub readList($\%) {
 my($file, $hash) = @_;
 my $in;
 if ($file eq '-') { $in = *STDIN }
 else { open $in, '<', $file or die "$0: $file: $!" }
 my $i = 0;
 while (<$in>) {
  chomp;
  s/\s+$//;
  next if /^$/ || /^\s*#/;
  $hash->{$_} = $i++;
 }
 return $i;
}

sub pushPair($$) {
 my($left, $top) = @_;
 ($left, $top) = ($top, $left) if $opts{T};
 $matrix{$left}{$top} = 1;
 $lefts{$left} = $rows++
  if $opts{S} && !defined $opts{1} && !exists $lefts{$left};
 $tops{$top} = $cols++ if $opts{S} && !defined $opts{2} && !exists $tops{$top};
}

__END__

=pod

=head1 NAME

B<binheat> - binary heat map generator

=head1 SYNOPSIS

B<binheat> [B<-1> I<file>] [B<-2> I<file>] [B<-mST>] [I<infile>]

=head1 DESCRIPTION

B<binheat> converts a description of a binary relation into an Embedded
PostScript image of the relation as a binary heat map (a.k.a. matrix display,
adjacency matrix, comparison chart, and probably a bunch of other names as
well).  I<infile> (or standard input if no file is specified) must list the
elements of the relation, one per line, each line consisting of two labels
(nonempty nontab character sequences) separated by one or more tabs.  (The
input may also contain comment lines in which the first nonwhitespace character
is C<#>.)  B<binheat> will then print an EPS file to standard output showing a
table in which the labels from the first column of each line are lexically
sorted along the left edge, the labels from the second column are lexically
sorted along the top edge, and dots are placed in the cells of the table to
represent the elements of the relation.

=head1 OPTIONS

=over

=item B<-1> I<file>

The lines of I<file> will taken as a list of all labels appearing in the first
column of the input file, and the labels along the left edge of the output
chart (or the top edge if B<-T> is in effect) will be in the same order that
they are listed in I<file>.  Labels that appear in I<file> but not the first
column of the input file will appear in the output with no relations, and
labels that appear in the first column of the input file but not I<file> will
not appear in the output at all.

This option overrides the B<-S> option for the first column only.

=item B<-2> I<file>

The lines of I<file> will taken as a list of all labels appearing in the second
column of the input file, and the labels along the top edge of the output chart
(or the left edge if B<-T> is in effect) will be in the same order that they
are listed in I<file>.  Labels that appear in I<file> but not the second column
of the input file will appear in the output with no relations, and labels that
appear in the second column of the input file but not I<file> will not appear
in the output at all.

This option overrides the B<-S> option for the second column only.

=item B<-m>

C<< foo<TAB>bar<TAB>baz >> (or any number of tab-separated fields) will be
allowed as an abbreviation for C<< foo<TAB>bar >> followed by C<< foo<TAB>baz
>> etc.

=item B<-S>

Labels in the output will be listed in the order in which they appear in the
input file rather than in lexical order

=item B<-T>

The output will be transposed -- i.e., the first column will be used for the
top edge of the chart and the second column for the left edge

=back

=head1 AUTHOR

John T. Wodder II <jwodder@sdf.lonestar.org>

=cut
