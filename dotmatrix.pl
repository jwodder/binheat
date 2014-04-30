#!/usr/bin/perl -w
# Options:
#   -1 file - list of all values for the first column in display order
#   -2 file - list of all values for the second column in display order
#   -T - use the first column for the top edge of the chart and the second
#        column for the left edge rather than the other way around
#   -S - display values in the order in which they appear in the input file
#        rather than sorted lexically (overridden by -1 and -2 options)
#   -m - allow "foo\tbar\tbaz\tglarch\n" as shorthand for
#        "\foo\tbar\nfoo\tbaz\nfoo\tglarch\n"
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
